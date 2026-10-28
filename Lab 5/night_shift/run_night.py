import bedtime
import report
import screen
import watch

# before bed -> overnight -> morning
if __name__ == "__main__":
    zone = bedtime.bedtime()
    watch.watch(zone)
    if not screen.HAS_SCREEN:
        input("press Enter for the morning report ")
    report.morning()
