from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
import requests

class ActionFetchSalesEvents(Action):
    def name(self) -> Text:
        return "action_fetch_sales_events"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = requests.get("https://localhost:7060/api/Sales", verify=False) 
        
        if response.status_code == 200:
          events = response.json().get('data', [])
          if events:
              message = "Tất cả các sự kiện sale:"
              for event in events:
                  message += f" Id: {event['id']} - {event['name']} - {event['description']}"
              message += f" Để biết thêm thông tin chi tiết sự kiện, vui lòng cung cấp cho chúng tôi biết id của sự kiện đó nhé!"
              dispatcher.utter_message(text=message)
          else:
              dispatcher.utter_message(text="Không có sự kiện sale nào.")
        else:
          dispatcher.utter_message(text="Đã có lỗi xảy ra khi lấy thông tin sự kiện sale.")
        return []

class ActionFetchSalesEventsCurrent(Action):
    def name(self) -> Text:
        return "action_fetch_sales_events_current"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = requests.get("https://localhost:7060/api/Sales/current", verify=False) 
        
        if response.status_code == 200:
          events = response.json().get('data', [])
          if events:
              message = "Các sự kiện sale hiện tại: "
              for event in events:
                  message += f"{event['name']} - {event['description']}. Dành cho: "
                  for customer in event['customerTypes']:
                      message += customer['name'] + ", "
                  message = message.rstrip(", ")
                  datetime_str2 = event['endDate']
                  datetime_obj2 = datetime.strptime(datetime_str2, '%Y-%m-%dT%H:%M:%S')
                  formatted_datetime2 = datetime_obj2.strftime('%Hh%Mp ngày %d/%m/%Y')
                  message += f" (Kết thúc lúc: {formatted_datetime2}); "
              dispatcher.utter_message(text=message)
          else:
              dispatcher.utter_message(text="Hiện không có sự kiện sale nào.")
        else:
          dispatcher.utter_message(text="Đã có lỗi xảy ra khi lấy thông tin sự kiện sale hiện tại.")
        return []

class ActionFetchSalesEventsUpcoming(Action):
    def name(self) -> Text:
        return "action_fetch_sales_events_upcoming"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = requests.get("https://localhost:7060/api/Sales/upcoming", verify=False) 
        
        if response.status_code == 200:
          events = response.json().get('data', [])
          if events:
              message = "Các sự kiện sale sắp tới: "
              for event in events:
                  message += f"{event['name']} - {event['description']}. Dành cho: "
                  for customer in event['customerTypes']:
                      message += customer['name'] + ", "

                  message = message.rstrip(", ")
                  message += f" (Bắt đầu lúc: "
                  datetime_str1 = event['startDate']
                  datetime_str2 = event['endDate']
                  datetime_obj1 = datetime.strptime(datetime_str1, '%Y-%m-%dT%H:%M:%S')
                  datetime_obj2 = datetime.strptime(datetime_str2, '%Y-%m-%dT%H:%M:%S')
                  formatted_datetime1 = datetime_obj1.strftime('%Hh%Mp ngày %d/%m/%Y')
                  formatted_datetime2 = datetime_obj2.strftime('%Hh%Mp ngày %d/%m/%Y')
                  message += f"{formatted_datetime1}, Kết thúc lúc: {formatted_datetime2}); "
              dispatcher.utter_message(text=message)
          else:
              dispatcher.utter_message(text="Sắp tới không có sự kiện sale nào.")
        else:
          dispatcher.utter_message(text="Đã có lỗi xảy ra khi lấy thông tin sự kiện sale sắp tới.")
        return []

class ActionFetchProductsCurrent(Action):
    def name(self) -> Text:
        return "action_fetch_products_current"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = requests.get("https://localhost:7060/api/Sales/current/products", verify=False) 
        
        if response.status_code == 200:
          events = response.json().get('data', [])
          if events:
              message = "Các sản phẩm đang sale hiện tại:"
              for event in events:
                  datetime_str2 = event['endDate']
                  datetime_obj2 = datetime.strptime(datetime_str2, '%Y-%m-%dT%H:%M:%S')
                  formatted_datetime2 = datetime_obj2.strftime('%Hh%Mp ngày %d/%m/%Y')
                  for product in event['products']:
                     message += f" {product['name']},"
                  message = message.rstrip(", ")    
                  message += f" (Kết thúc lúc: {formatted_datetime2}); "             
              dispatcher.utter_message(text=message)
          else:
              dispatcher.utter_message(text="Hiện không có sản phẩm nào sale.")
        else:
          dispatcher.utter_message(text="Đã có lỗi xảy ra khi lấy thông tin sản phẩm sale hiện tại.")
        return []

class ActionFetchProductsUpcoming(Action):
    def name(self) -> Text:
        return "action_fetch_products_upcoming"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        response = requests.get("https://localhost:7060/api/Sales/upcoming/products", verify=False) 
        
        if response.status_code == 200:
          events = response.json().get('data', [])
          if events:
              message = "Các sản phẩm sale sắp tới: "
              for event in events:
                  for product in event['products']:
                     message += f" {product['name']},"
                  message = message.rstrip(", ") 
                  message += f" (Bắt đầu lúc: "
                  datetime_str1 = event['startDate']
                  datetime_str2 = event['endDate']
                  datetime_obj1 = datetime.strptime(datetime_str1, '%Y-%m-%dT%H:%M:%S')
                  datetime_obj2 = datetime.strptime(datetime_str2, '%Y-%m-%dT%H:%M:%S')
                  formatted_datetime1 = datetime_obj1.strftime('%Hh%Mp ngày %d/%m/%Y')
                  formatted_datetime2 = datetime_obj2.strftime('%Hh%Mp ngày %d/%m/%Y')
                  message += f"{formatted_datetime1}, Kết thúc lúc: {formatted_datetime2}); "
              dispatcher.utter_message(text=message)
          else:
              dispatcher.utter_message(text="Sắp tới không có sản phẩm sale nào.")
        else:
          dispatcher.utter_message(text="Đã có lỗi xảy ra khi lấy thông tin sản phẩm sale sắp tới.")
        return []

class ActionFetchSalesEventById(Action):
    def name(self) -> Text:
        return "action_fetch_sales_event_by_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        event_id = tracker.get_slot('event_id')

        try:
            event_id = int(event_id)
        except ValueError:
            dispatcher.utter_message(text="ID không hợp lệ. Vui lòng cung cấp ID hợp lệ.")
            return []   
     
        if event_id:
            response = requests.get(f"https://localhost:7060/api/Sales/{event_id}", verify=False)
            if response.status_code == 200:
                event = response.json()
                message = "Sự kiện sale được tìm: "
                message += f"{event['name']} - {event['description']}, dành cho: "
                for customer in event['customerTypes']:
                    message += customer['name'] + ", "

                message = message.rstrip(", ")
                message += f" (Bắt đầu lúc: "
                datetime_str1 = event['startDate']
                datetime_str2 = event['endDate']
                datetime_obj1 = datetime.strptime(datetime_str1, '%Y-%m-%dT%H:%M:%S')
                datetime_obj2 = datetime.strptime(datetime_str2, '%Y-%m-%dT%H:%M:%S')
                formatted_datetime1 = datetime_obj1.strftime('%Hh%Mp ngày %d/%m/%Y')
                formatted_datetime2 = datetime_obj2.strftime('%Hh%Mp ngày %d/%m/%Y')
                message += f"{formatted_datetime1}, Kết thúc lúc: {formatted_datetime2}). Các sản phẩm được sale: "
                for product in event['products']:
                   message += f" {product['name']},"
                message = message.rstrip(", ")
                message += f"."
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text=f"Không tìm thấy sự kiện với ID {event_id}.")
        else:
            dispatcher.utter_message(text="Bạn vui lòng cung cấp ID của sự kiện.")
        
        return []
