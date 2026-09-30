import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
SCHEDULE_FILE = Path(__file__).with_name("schedule.json")


def load_schedule():
    """schedule.json を読み込んで、予定のリストを返す。"""
    try:
        with SCHEDULE_FILE.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{SCHEDULE_FILE.name} が見つかりません。schedule.py と同じフォルダに置いてください。")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"{SCHEDULE_FILE.name} の形式が正しくありません: {e}")
        sys.exit(1)


def filter_by_date(events, date_str):
    """指定した日（YYYY-MM-DD）の予定だけを、開始時刻の順に並べて返す。"""
    same_day = [e for e in events if e["start"].startswith(date_str)]
    return sorted(same_day, key=lambda e: e["start"])


def format_event(event):
    """予定1件を1行の文字列にする。"""
    start = event["start"].split("T")[1]
    end = event["end"].split("T")[1]
    location = event.get("location", "（場所なし）")
    return f"{start}-{end}  {event['title']}  @{location}"


def main():
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.now(JST).strftime("%Y-%m-%d")

    events = load_schedule()
    todays = filter_by_date(events, date_str)

    print(f"{date_str} の予定 {len(todays)} 件")
    for event in todays:
        print(format_event(event))


if __name__ == "__main__":
    main()
