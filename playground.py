from datetime import datetime as dt


now = dt.now().strftime("%H:%M | %d %B %Y")

print(now)

print(now.split("|"))
