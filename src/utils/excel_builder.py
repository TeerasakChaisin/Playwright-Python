from openpyxl import Workbook
from datetime import datetime, timedelta

def build_tier_update_excel(member_ids, config, path):
    wb = Workbook()
    ws = wb.active
    ws.append(["member_id", "tier_code"])

    rules = config.get("rules", [])
    default_code = config["default"]["tier_code"]

    index = 0

    for rule in rules:
        code = rule["tier_code"]
        amount = rule["amount"]

        for m in member_ids[index:index + amount]:
            ws.append([m, code])

        index += amount

    for m in member_ids[index:]:
        ws.append([m, default_code])

    wb.save(path)


def build_wallet_excel(member_ids, columns, path):
    wb = Workbook()
    ws = wb.active

    headers = ["member_id"] + list(columns.keys())
    ws.append(headers)

    for m in member_ids:
        row = [m]

        for k, v in columns.items():
            if v == "auto" and k == "expired_at":
                v = (datetime.now() + timedelta(days=30)).strftime("%d-%b-%Y")
            elif v in (None, "", "null"):
                v = ""
            row.append(v)

        ws.append(row)

    wb.save(path)
