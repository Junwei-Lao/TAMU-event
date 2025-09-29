import requests
from bs4 import BeautifulSoup
import time
import random

blackList = ["Transit: No Service",
        "Transit Break Service",
        "Faculty and Staff Holiday",
        "First Day of Classes",
        "First Friday Downtown Bryan Shuttle",
        "Transit Fall Service - Last Day",
        "CLOSED"]


websiteList = ["https://calendar.tamu.edu/tamu/month/date/", "http://calendar.tamu.edu/successcenter/month/date/",
"http://calendar.tamu.edu/academyarts/month/date/","http://calendar.tamu.edu/athletics/month/date/",
"https://calendar.tamu.edu/AOS/month/date/","https://calendar.tamu.edu/apcc/month/date/",
"https://calendar.tamu.edu/ais/month/date/","http://calendar.tamu.edu/abs/month/date/",
"https://calendar.tamu.edu/atmos-science/month/date/","https://calendar.tamu.edu/bushschool/month/date/",
"https://calendar.tamu.edu/careercenter/month/date/","http://calendar.tamu.edu/cte/month/date/",
"https://calendar.tamu.edu/codhr/month/date/","https://calendar.tamu.edu/cecr/month/date/",
"http://calendar.tamu.edu/chemistry-roadshow/month/date/","http://calendar.tamu.edu/cirtl/month/date/",
"http://calendar.tamu.edu/cbhec/month/date/","https://calendar.tamu.edu/architecture/month/date/",
"https://calendar.tamu.edu/artsci/month/date/","https://calendar.tamu.edu/artsci-ord/month/date/",
"https://calendar.tamu.edu/cehd/month/date/","http://calendar.tamu.edu/engineering/month/date/",
"https://calendar.tamu.edu/aero/month/date/","https://calendar.tamu.edu/bmen/month/date/",
"https://calendar.tamu.edu/chen/month/date/","https://calendar.tamu.edu/csce/month/date/",
"https://calendar.tamu.edu/ecen/month/date/","https://calendar.tamu.edu/eh/month/date/",
"https://calendar.tamu.edu/engineering-seminars/month/date/","https://calendar.tamu.edu/etid/month/date/",
"https://calendar.tamu.edu/isen/month/date/","https://calendar.tamu.edu/msen/month/date/",
"https://calendar.tamu.edu/mtde/month/date/","https://calendar.tamu.edu/nuen/month/date/",
"https://calendar.tamu.edu/ocen/month/date/","https://calendar.tamu.edu/cven/month/date/",
"https://calendar.tamu.edu/medicine/month/date/","https://calendar.tamu.edu/nursing/month/date/",
"https://calendar.tamu.edu/pvfa/month/date/","https://calendar.tamu.edu/vetmed/month/date/",
"https://calendar.tamu.edu/collaborations/month/date/","https://calendar.tamu.edu/cfr/month/date/",
"http://calendar.tamu.edu/corps/month/date/","http://calendar.tamu.edu/anthropology/month/date/",
"https://calendar.tamu.edu/deptofarchitecture/month/date/","http://calendar.tamu.edu/biology/month/date/",
"https://calendar.tamu.edu/chemistry/month/date/","https://calendar.tamu.edu/communication/month/date/",
"http://calendar.tamu.edu/economics/month/date/","http://calendar.tamu.edu/eahr/month/date/",
"http://calendar.tamu.edu/epsy/month/date/","http://calendar.tamu.edu/english/month/date/",
"https://calendar.tamu.edu/glac/month/date/","http://calendar.tamu.edu/hlkn/month/date/",
"http://calendar.tamu.edu/history/month/date/","https://calendar.tamu.edu/math/month/date/",
"http://calendar.tamu.edu/philosophy/month/date/","http://calendar.tamu.edu/psychology/month/date/",
"https://calendar.tamu.edu/deptrecsports/month/date/","https://calendar.tamu.edu/reslife/month/date/",
"http://calendar.tamu.edu/sociology/month/date/","http://calendar.tamu.edu/statistics/month/date/",
"http://calendar.tamu.edu/tlac/month/date/","https://calendar.tamu.edu/disability/month/date/",
"https://calendar.tamu.edu/academic-affairs/month/date/","https://calendar.tamu.edu/eeb/month/date/",
"http://calendar.tamu.edu/educationabroad/month/date/","http://calendar.tamu.edu/emergency/month/date/",
"http://calendar.tamu.edu/energy/month/date/","https://calendar.tamu.edu/elp/month/date/",
"https://calendar.tamu.edu/faculty-affairs/month/date/","http://calendar.tamu.edu/family-weekend/month/date/",
"https://calendar.tamu.edu/admissions/month/date/","https://calendar.tamu.edu/gradaggies/month/date/",
"https://calendar.tamu.edu/geography/month/date/","https://calendar.tamu.edu/geology-geophysics/month/date/",
"https://calendar.tamu.edu/glasscockcenter/month/date/","https://calendar.tamu.edu/global-engagement/month/date/",
"http://calendar.tamu.edu/goweb/month/date/","https://calendar.tamu.edu/graduatestudies/month/date/",
"http://calendar.tamu.edu/healthy-texas/month/date/","https://calendar.tamu.edu/hprc/month/date/",
"https://calendar.tamu.edu/HECMcAllen/month/date/","https://calendar.tamu.edu/honorsacademy/month/date/",
"https://calendar.tamu.edu/howdy-week/month/date/","https://calendar.tamu.edu/employees/month/date/",
"http://calendar.tamu.edu/ibt/month/date/","https://calendar.tamu.edu/int-ocean-drilling/month/date/",
"https://calendar.tamu.edu/education-week/month/date/","https://calendar.tamu.edu/isss/month/date/",
"https://calendar.tamu.edu/pharmacy/month/date/","https://calendar.tamu.edu/kamu-community/month/date/",
"https://calendar.tamu.edu/law/month/date/","https://calendar.tamu.edu/libraries/month/date/",
"https://calendar.tamu.edu/mays/month/date/","https://calendar.tamu.edu/meen/month/date/",
"https://calendar.tamu.edu/milvetnet/month/date/","https://calendar.tamu.edu/msc/month/date/",
"https://calendar.tamu.edu/music-activities/month/date/","http://calendar.tamu.edu/national-fellowships/month/date/",
"https://calendar.tamu.edu/oceanography/month/date/","https://calendar.tamu.edu/studentsuccess/month/date/",
"https://calendar.tamu.edu/youthengagement/month/date/","https://calendar.tamu.edu/brand-development/month/date/",
"https://calendar.tamu.edu/sustainability/month/date/","https://calendar.tamu.edu/president/month/date/",
"https://calendar.tamu.edu/registrar/month/date/","https://calendar.tamu.edu/ugr/month/date/",
"https://calendar.tamu.edu/opas/month/date/","https://calendar.tamu.edu/opsa/month/date/",
"https://calendar.tamu.edu/pete/month/date/","http://calendar.tamu.edu/phikappaphi/month/date/",
"http://calendar.tamu.edu/physics/month/date/","https://calendar.tamu.edu/pas/month/date/",
"http://calendar.tamu.edu/perc/month/date/","https://calendar.tamu.edu/provost/month/date/",
"https://calendar.tamu.edu/pito/month/date/","http://calendar.tamu.edu/resi/month/date/",
"https://calendar.tamu.edu/recsports/month/date/","https://calendar.tamu.edu/research/month/date/",
"http://calendar.tamu.edu/rds/month/date/","https://calendar.tamu.edu/ric/month/date/",
"http://calendar.tamu.edu/rchi/month/date/","http://calendar.tamu.edu/sfaid/month/date/",
"https://calendar.tamu.edu/engineeringmedicine/month/date/","https://calendar.tamu.edu/sph/month/date/",
"https://calendar.tamu.edu/studentactivities/month/date/","https://calendar.tamu.edu/dsa/month/date/",
"https://calendar.tamu.edu/sbs/month/date/","https://calendar.tamu.edu/student-interest/month/date/",
"https://calendar.tamu.edu/student-life/month/date/","https://calendar.tamu.edu/postdoctoral-association/month/date/",
"https://calendar.tamu.edu/tamu-it/month/date/","https://calendar.tamu.edu/agrilife/month/date/",
"https://calendar.tamu.edu/dentistry/month/date/","https://calendar.tamu.edu/tees/month/date/",
"https://calendar.tamu.edu/tfs/month/date/","https://calendar.tamu.edu/forensic-nursing/month/date/",
"https://calendar.tamu.edu/hsc/month/date/","https://calendar.tamu.edu/tam-innovation/month/date/",
"https://calendar.tamu.edu/nursing-mobile-clinic/month/date/","https://calendar.tamu.edu/qatar/month/date/",
"https://calendar.tamu.edu/txrdc/month/date/","https://calendar.tamu.edu/texas-sea-grant/month/date/",
"https://calendar.tamu.edu/twri/month/date/","https://calendar.tamu.edu/afs/month/date/",
"https://calendar.tamu.edu/nlo/month/date/","http://calendar.tamu.edu/toxicology/month/date/",
"http://calendar.tamu.edu/university-arts/month/date/","http://calendar.tamu.edu/dining/month/date/",
"https://calendar.tamu.edu/uhs/month/date/","https://calendar.tamu.edu/libraries-annex/month/date/",
"http://calendar.tamu.edu/upd/month/date/","http://calendar.tamu.edu/writingcenter/month/date/",
"https://calendar.tamu.edu/Veteran-Resource-Support-Center/month/date/","https://calendar.tamu.edu/water-management/month/date/",
"https://calendar.tamu.edu/wan/month/date/","https://calendar.tamu.edu/wgst/month/date/"
]


daylist = ['20250101', '20250201', '20250301', '20250401', '20250501', '20250601', '20250701', '20250801', '20250901', '20251001', '20251101', '20251201']

init = "?user_tz=America%2FChicago&template_vars=id,time,title_link,summary,until,repeats,is_multi_day,is_first_multi_day,multi_day_span,href,tag_classes,category_classes&syntax="

init2 = "?user_tz=America%2FChicago&template_vars=group,title,date_time,add_to_google,add_to_yahoo,ical_download_href,repeats,until,location,custom_room_number,summary,description,contact_info,related_content,cost,registration,tags_calendar,id,image,online_url,online_button_label,online_instructions,share_links,has_tags,is_repeating,has_cost,has_registration,is_online,location_latitude&syntax="


eventpage = "https://calendar.tamu.edu/event/"
eventpage_starter = "https://calendar.tamu.edu/live/calendar/view/event/slug/"


headers = [
    # Windows - Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/124.0.2478.67 Safari/537.36",

    # macOS - Chrome / Safari / Firefox
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) Gecko/20100101 Firefox/124.0",

    # Linux - Chrome / Firefox
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",

    # iPhone / iOS Safari
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",

    # Android - Chrome / Samsung Internet
    "Mozilla/5.0 (Linux; Android 14; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-G996U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/110.0.5481.153 Mobile Safari/537.36",
]

hearderIndex = 0
refreshtime = 60

with open("data.txt", "w", encoding="utf-8") as f:
  for j, base_url in enumerate(websiteList):
      for k in daylist:
          url = base_url + k

          while True:
            try:
                response0 = requests.get(url, headers={"User-Agent": headers[hearderIndex]})
                soup = BeautifulSoup(response0.text, "html.parser")

                div = soup.find("div", class_="lw_widget_syntax lw_hidden")

                if not div:   # <--- guard
                    raise ValueError("Div not found")

                div_title = div.get("title")
                if not div_title:
                    raise ValueError("Div title not found")

                # Success
                break

            except Exception as e:
                print(f"No hidden syntax div found for {url}, waiting seconds: {refreshtime}, error: {e}")
                if refreshtime >= 600:
                    break
                time.sleep(refreshtime)
                refreshtime = refreshtime * 2 + random.uniform(-10, 10)
                hearderIndex = (hearderIndex + 1) % len(headers)
                continue

          if refreshtime >= 600:
                print("refreshtime >= 600. Something went wrong. Skip this event")
                refreshtime = 60 + round(random.uniform(-5.0, 5.0), 2)
                continue


          url2 = "https://calendar.tamu.edu/live/calendar/view/month/date/" + k + init + div_title
          response = requests.get(url2, headers={"User-Agent": headers[hearderIndex]})
          refreshtime = 60 + round(random.uniform(-5.0, 5.0), 2)


          try:
                events_json = response.json().get("days", [])
          except ValueError as e:
                print(f"JSON decode failed at {url2}: {e}")
                continue


          for event in events_json:
              if event.get("class_name") != "lw_cal_rollover_month" and event.get("event_count") != 0:

                  print("here2, ", event.get("date"))

                  for event_day_specific in event.get("events", []):

                      print("here3")

                      event_split = event_day_specific.get("href", "").split("/")

                      summary = BeautifulSoup(event_day_specific.get("summary", ""), "html.parser").get_text(strip=True)
                      title = BeautifulSoup(event_day_specific.get("title", ""), "html.parser").get_text(strip=True)

                      if len(event_split) <= 0 :
                            print("no avaliable link on this event")
                            continue


                      event_id = event_split[-1]
                      event_start = event_split[0]


                      if (event_start == "event"):
                            #Now get into the second page

                            #get webpage
                            while True:
                                try:
                                    html_content2 = requests.get(eventpage+event_id, headers={"User-Agent": headers[hearderIndex]})
                                    soup2 = BeautifulSoup(html_content2.text, "html.parser")
                                    div2 = soup2.find("div", class_="lw_widget_syntax lw_hidden")

                                    if not div2:   # <--- guard
                                        raise ValueError("Div2 not found")

                                    div2_title_url = div2.get("title")
                                    if not div2_title_url:
                                        raise ValueError("Div2_title_url not found")

                                    # Success
                                    break

                                except Exception as e:
                                    print(f"No detail div for event {event_id}, waiting seconds: {refreshtime}, error: {e}")
                                    if refreshtime >= 600:
                                        break
                                    time.sleep(refreshtime)
                                    refreshtime = refreshtime * 2 + random.uniform(-10, 10)

                                    hearderIndex = (hearderIndex + 1) % len(headers)
                                    continue

                            if refreshtime >= 600:
                                    print("refreshtime >= 600. Something went wrong. Skip this event")
                                    refreshtime = 60 + round(random.uniform(-5.0, 5.0), 2)
                                    continue
                            
                            #get webpage json file
                            url3 = eventpage_starter + event_id + init2 + div2_title_url
                            response2 = requests.get(url3, headers={"User-Agent": headers[hearderIndex]})
                            refreshtime = 60 + round(random.uniform(-5.0, 5.0), 2)


                            if "application/json" not in response2.headers.get("Content-Type", ""):
                                    print(f"Not JSON at {url3}")
                                    continue


                            try:
                                events_json2 = response2.json()

                                event_date = events_json2["title"]

                                title = events_json2["event"]["title"]
                                if (title in blackList):
                                        print(f"Title in blackList: {title}")
                                        continue

                                description = events_json2["event"]["description"]

                                text = title + ". " + summary + " " + BeautifulSoup(description, "html.parser").get_text(strip=True)

                                if len(text) <= 1:
                                        print("len(text) <= 1")
                                        continue

                                print(text)
                                f.write(text + "\n")

                            except Exception as e:
                                print(f"Extraction failed at {url3}: {e}")
                      else:
                            print("Detected external website. Keep title and summary only")

                            text = title + ". " + summary

                            if len(text) <= 1:
                                print("len(text) <= 1")
                                continue

                            print(text)
                            f.write(text + "\n")


              hearderIndex = (hearderIndex + 1) % len(headers)
