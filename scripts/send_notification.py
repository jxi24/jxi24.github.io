#!/usr/bin/env python3
"""
Send an HTML email notification for newly synced publications.

Reads the JSON produced by sync_publications.py, builds an HTML email,
and sends it via SMTP with preview images as attachments.

All SMTP settings are read from environment variables (ideal for CI) or
can be passed as CLI flags for local testing.

Required env vars (or equivalent flags):
    SMTP_SERVER        hostname, e.g. smtp.gmail.com
    SMTP_USER          login / sender address
    SMTP_PASSWORD      password or app-password

Optional env vars:
    SMTP_PORT          465 (SSL, default) or 587 (STARTTLS)
    NOTIFICATION_EMAIL recipient; defaults to isaacson@fnal.gov

Usage:
    # In CI (env vars set as secrets)
    python3 scripts/send_notification.py --json /tmp/new_papers.json

    # Local test
    python3 scripts/send_notification.py \\
        --json /tmp/new_papers.json \\
        --smtp-server smtp.gmail.com \\
        --smtp-user you@gmail.com \\
        --smtp-password "app-password" \\
        --to isaacson@fnal.gov
"""

import argparse
import json
import os
import smtplib
import sys
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

DEFAULT_TO = "isaacson@fnal.gov"
DEFAULT_PORT = 465


def _clean(text: str, max_len: int = 0) -> str:
    """Strip outer BibTeX braces/quotes; optionally truncate."""
    text = text.strip().strip('{}').strip('"').strip()
    if max_len and len(text) > max_len:
        text = text[:max_len - 1] + "\u2026"
    return text


def build_html(papers: list[dict]) -> str:
    n = len(papers)
    rows: list[str] = []
    for p in papers:
        title = _clean(p.get("title", "(untitled)"))
        authors = _clean(p.get("authors", ""), max_len=140)
        arxiv = p.get("arxiv", "")
        inspire_id = p.get("inspire_id")

        links: list[str] = []
        if arxiv:
            links.append(
                f'<a href="https://arxiv.org/abs/{arxiv}" style="color:#0056b3">'
                f"arXiv:{arxiv}</a>"
            )
        if inspire_id:
            links.append(
                f'<a href="https://inspirehep.net/literature/{inspire_id}" '
                f'style="color:#0056b3">InspireHEP</a>'
            )
        link_html = " &nbsp;·&nbsp; ".join(links)

        rows.append(
            f"""<tr>
  <td style="padding:14px 0;border-bottom:1px solid #e5e5e5;vertical-align:top">
    <div style="font-size:1.0em;font-weight:600;color:#111;margin-bottom:3px">{title}</div>
    <div style="font-size:0.88em;color:#555;margin-bottom:5px">{authors}</div>
    <div style="font-size:0.85em">{link_html}</div>
  </td>
</tr>"""
        )

    paper_word = "paper" if n == 1 else "papers"
    was_were = "was" if n == 1 else "were"

    return f"""<!DOCTYPE html>
<html lang="en">
<body style="margin:0;padding:0;background:#f4f4f4;font-family:-apple-system,
  BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0">
  <tr><td align="center" style="padding:32px 16px">
    <table width="620" cellpadding="0" cellspacing="0"
           style="background:#fff;border-radius:6px;
                  box-shadow:0 1px 4px rgba(0,0,0,.12)">
      <tr>
        <td style="padding:28px 32px 20px;border-bottom:3px solid #222">
          <h1 style="margin:0;font-size:1.25em;color:#111">
            {n} new {paper_word} synced to jxi24.github.io
          </h1>
        </td>
      </tr>
      <tr>
        <td style="padding:16px 32px 0">
          <p style="margin:0 0 16px;color:#444;font-size:0.95em">
            The following {paper_word} {was_were} found on InspireHEP / ORCID and
            added to your bibliography. Preview images are attached.
          </p>
          <table width="100%" cellpadding="0" cellspacing="0"
                 style="border-collapse:collapse">
            {"".join(rows)}
          </table>
        </td>
      </tr>
      <tr>
        <td style="padding:20px 32px 28px">
          <p style="margin:0;padding:12px 16px;background:#f8f8f8;
                    border-left:3px solid #ccc;border-radius:3px;
                    font-size:0.83em;color:#666;line-height:1.6">
            To feature a paper on your about page add
            <code style="background:#ebebeb;padding:1px 4px;border-radius:3px">
              selected = {{true}}</code> in
            <code style="background:#ebebeb;padding:1px 4px;border-radius:3px">
              _bibliography/papers.bib</code>.<br>
            Replace <code style="background:#ebebeb;padding:1px 4px;border-radius:3px">
              preview = {{default.png}}</code> with a real thumbnail in
            <code style="background:#ebebeb;padding:1px 4px;border-radius:3px">
              assets/img/publication_preview/</code>.
          </p>
        </td>
      </tr>
    </table>
  </td></tr>
</table>
</body>
</html>"""


def send(
    papers: list[dict],
    preview_dir: Path,
    smtp_server: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    to_addr: str,
) -> None:
    n = len(papers)
    subject = (
        f"{n} new publication{'s' if n != 1 else ''} synced to jxi24.github.io"
    )

    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = f"Portfolio Bot <{smtp_user}>"
    msg["To"] = to_addr

    msg.attach(MIMEText(build_html(papers), "html", "utf-8"))

    attached = 0
    for p in papers:
        img_path = preview_dir / p.get("preview", "")
        if img_path.exists():
            img_part = MIMEImage(img_path.read_bytes(), name=img_path.name)
            img_part.add_header(
                "Content-Disposition", "attachment", filename=img_path.name
            )
            msg.attach(img_part)
            attached += 1

    print(f"Sending to {to_addr} via {smtp_server}:{smtp_port} ({attached} attachment(s))...")

    if smtp_port == 587:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as srv:
            srv.starttls()
            srv.login(smtp_user, smtp_password)
            srv.send_message(msg)
    else:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30) as srv:
            srv.login(smtp_user, smtp_password)
            srv.send_message(msg)

    print("Email sent.")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Email notification for newly synced publications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--json", required=True,
                    help="JSON output file from sync_publications.py")
    ap.add_argument("--preview-dir", default="assets/img/publication_preview")
    ap.add_argument("--smtp-server",
                    default=os.environ.get("SMTP_SERVER"),
                    help="SMTP hostname (env: SMTP_SERVER)")
    ap.add_argument("--smtp-port", type=int,
                    default=int(os.environ.get("SMTP_PORT", DEFAULT_PORT)),
                    help=f"SMTP port (env: SMTP_PORT, default: {DEFAULT_PORT})")
    ap.add_argument("--smtp-user",
                    default=os.environ.get("SMTP_USER"),
                    help="SMTP login / sender address (env: SMTP_USER)")
    ap.add_argument("--smtp-password",
                    default=os.environ.get("SMTP_PASSWORD"),
                    help="SMTP password or app-password (env: SMTP_PASSWORD)")
    ap.add_argument("--to",
                    default=os.environ.get("NOTIFICATION_EMAIL", DEFAULT_TO),
                    help=f"Recipient address (env: NOTIFICATION_EMAIL, default: {DEFAULT_TO})")
    args = ap.parse_args()

    missing = [v for v in ("smtp_server", "smtp_user", "smtp_password")
               if not getattr(args, v)]
    if missing:
        print(f"SMTP not configured ({', '.join(missing)} missing) — skipping email.")
        print("Set SMTP_SERVER, SMTP_USER, SMTP_PASSWORD as env vars or CLI flags.")
        return

    data = json.loads(Path(args.json).read_text())
    papers = data.get("new_papers", [])
    if not papers:
        print("JSON contains no new papers — nothing to send.")
        return

    try:
        send(
            papers=papers,
            preview_dir=Path(args.preview_dir),
            smtp_server=args.smtp_server,
            smtp_port=args.smtp_port,
            smtp_user=args.smtp_user,
            smtp_password=args.smtp_password,
            to_addr=args.to,
        )
    except smtplib.SMTPException as exc:
        print(f"SMTP error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
