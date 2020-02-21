from requests import get
from bs4 import BeautifulSoup
import csv

rows = []
categories = ['delivery', 'reservations', 'burgers', 'italian', 'takeout', 'waitlist', 'chinese', 'mexican',
              'contractors', 'electricians', 'homecleaning', 'hvac', 'landscaping', 'locksmiths', 'movers', 'plumbing',
              'autorepair', 'auto_detailing', 'bodyshops', 'carwash', 'car_dealers', 'oilchange', 'parking', 'towing',
              ]
try:
    for category in categories:
        # making writer object with current category name
        file = open(category + ".csv", 'a')
        writer = csv.writer(file)
        # appending first row for column names
        rows.append(
            ['Title', 'Address', 'Site', 'Contact_number', 'About_business', 'Amneties', 'Working_hours', 'QnA'])
        main_page_url = 'https://www.yelp.com/search?find_desc=' + category + '&find_loc=New+York%2C+NY%2C+US'
        response = get(main_page_url)
        Main_Page = BeautifulSoup(response.text, 'html.parser')
        # loop for 20 pages per category
        for i in range(0, 20):
            if i == 0:  # passing first iteration because we first scrap the current page
                pass
            else:  # changing the main_page_url and navigation to next page
                pagination = Main_Page.find("div", {
                    "class": "lemon--div__373c0__1mboc pagination-links__373c0__3CXzO border-color--default__373c0__3-ifU nowrap__373c0__35McF"})
                link = pagination.find('a', {
                    "class": "lemon--a__373c0__IEZFH link__373c0__1G70M next-link navigation-button__373c0__23BAT link-color--inherit__373c0__3dzpk link-size--inherit__373c0__1VFlE"})
                main_page_url = "https://www.yelp.com" + str(link['href'])
                response = get(main_page_url)
                Main_Page = BeautifulSoup(response.text, 'html.parser')

            All_items = Main_Page.find_all("div", {
                "class": "lemon--div__373c0__1mboc container__373c0__ZB8u4 hoverable__373c0__3CcYQ margin-t3__373c0__1l90z margin-b3__373c0__q1DuY padding-t3__373c0__1gw9E padding-r3__373c0__57InZ padding-b3__373c0__342DA padding-l3__373c0__1scQ0 border--top__373c0__3gXLy border--right__373c0__1n3Iv border--bottom__373c0__3qNtD border--left__373c0__d1B7K border-color--default__373c0__3-ifU"})
            for item in All_items:
                # added try catch because if the single items fails due to any reason then the whole execution will continue
                try:
                    if All_items.index(item) > 0:
                        Item_url = "https://www.yelp.com" + item.a["href"]
                        response2 = get(Item_url)
                        Single_item_page = BeautifulSoup(response2.text, 'html.parser')
                        title = Single_item_page.find("h1", {
                            "class": "lemon--h1__373c0__2ZHSL heading--h1__373c0__1VUMO heading--no-spacing__373c0__"
                                     "1PzQP heading--inline__373c0__1F-Z6"}).text
                        info = Single_item_page.find("div", {
                            "class": "lemon--div__373c0__1mboc island__373c0__3fs6U u-padding-t1 u-padding-r1 u-padding"
                                     "-b1 u-padding-l1 border--top__373c0__19Owr border--right__373c0__22AHO border"
                                     "--bottom__373c0__uPbXS border--left__373c0__1SjJs border-color"
                                     "--default__373c0__2oFDT background-color--white__373c0__GVEnp"})
                        # checking if site contains a website and assigning empty if not
                        site = info.a.text
                        if "." in site:
                            pass
                        else:
                            site = ''
                        ################################################ ALEEM CODE ##################################
                        contact_number = info.find("p", {
                            "class": "lemon--p__373c0__3Qnnj text__373c0__2pB8f text-color--normal__373c0__K_MKN text-align--left__373c0__2pnx_"}).text
                        #######
                        # business = Single_item_page.find_All("section", {
                        #     "class": "lemon--section__373c0__fNwDM u-space-t4 u-padding-t4 border--top__373c0__19Owr border-color--default__373c0__2oFDT"})
                        # business = business[3]
                        # business = business.find_All("span")
                        # b1 = business[0].text
                        # # b2 = business[1].text ####(b2 me about business ka dosra part he agar lagana ho tu uncomment kar de warna hata de)####
                        # about_business = b1  # +b2
                        #######
                        qna = Single_item_page.find("section", {
                            "class": "lemon--section__373c0__fNwDM u-space-t4 u-padding-t4 border--top__373c0__19Owr border-color--default__373c0__2oFDT"})
                        QnA_field = qna[4].div.ul.findall("div", {
                            "class": "lemon--div__373c0__1mboc arrange-unit__373c0__1piwO arrange-unit-fill__373c0__17z0h border-color--default__373c0__2oFDT"})
                        q1 = QnA_field[0].text
                        a1 = QnA_field[1].text
                        q2 = QnA_field[2].text
                        a2 = QnA_field[3].text
                        QnA = {"Q1 : ": q1, "A1 : ": a1, "Q2 : ": q2, "A2 : ": a2}
                        ##################################################          ###################################

                        # fetching whole amenities card
                        Amenities_card = Single_item_page.find('div', {
                            "class": "lemon--div__373c0__1mboc arrange__373c0__UHqhV gutter-12__373c0__3kguh layout-wrap__373c0__34d4b layout-2-units__373c0__3CiAk border-color--default__373c0__2oFDT"})
                        amneties = {}
                        for amnety in Amenities_card:
                            # fetching each amenity div
                            data = amnety.find('div', {
                                'class': 'lemon--div__373c0__1mboc arrange-unit__373c0__1piwO arrange-unit-fill__373c0__17z0h border-color--default__373c0__2oFDT'}).contents
                            for text in data:
                                # iterating through all available amenities and making a dictionary name amenities with key and values
                                # passing on P element because it contain details of amenity nor key,value
                                if text.name == 'p':
                                    pass
                                elif data.index(text) % 2 == 0:
                                    key = text.text
                                else:
                                    value = text.text
                            amneties[key] = value
                        # fetching a whole container containing address and working hours and then separating both
                        detail_container = Single_item_page.find("div", {
                            "class": "lemon--div__373c0__1mboc arrange__373c0__UHqhV gutter-30__373c0__2PiuS border-color"
                                     "--default__373c0__2oFDT"})
                        address = detail_container.find('address', {"class": "lemon--address__373c0__2sPac"}).text
                        working_hours_table = detail_container.find('tbody', {
                            "class": "lemon--tbody__373c0__2T6Pl"})
                        working_days_and_hours = {}
                        for single_day in working_hours_table:
                            days = single_day.find('th', {
                                "class": "lemon--th__373c0__2EYOe table-header-cell__373c0__3vHHa table-header-cell__373c0___pz7p"}).p.text
                            hours_component = single_day.find('td', {
                                "class": "lemon--td__373c0__gBfiC table-cell__373c0__HrAej table-cell__373c0__2eOj9 table-cell--top__373c0__2WIt-"})
                            hours = hours_component.find('ul', {
                                "class": "lemon--ul__373c0__1_cxs undefined list__373c0__2G8oH"}).text
                            # Making a dictionary for all week days and hours
                            working_days_and_hours[days] = hours
                        # appending all values in a list name rows to write in csv at once
                        rows.append(
                            [title, address, site, contact_number, amneties, working_days_and_hours,
                             QnA])
                    else:
                        pass
                except Exception as e:
                    print(e.__str__())
                    pass

        writer.writerows(rows)
except Exception as e:
    print(e.__str__())
