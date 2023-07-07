import requests
import pandas as pd

class CrawlCellphone:
    def __init__(self):
        self.url = 'https://api.cellphones.com.vn/v2/graphql/query'
        self.headers = {'Content-Type': 'application/json'}
    
    def get_list_phone(self, nums):
        data = {
            'query': f'''
                query {{
                    products(
                        filter: {{
                            static: {{
                                categories: ["3"],
                                province_id: 30,
                                stock: {{ from: 0 }},
                                stock_available_id: [46, 56, 152],
                                filter_price: {{ from: 0, to: 55990000 }}
                            }},
                            dynamic: {{}}
                        }},
                        page: 1,
                        size: {nums},
                        sort: [{{ view: "desc" }}]
                    ) {{
                        general {{
                            product_id
                            name
                            attributes
                            manufacturer
                            url_path
                        }},
                        filterable {{
                            price
                            special_price
                        }}
                    }}
                }}
            '''
        }
        response = requests.post(self.url, headers=self.headers, json=data)
        return response.json()
    
    def get_info_phone(self, data):
        output = []
        for i in range(len(data['data']['products'])):
            try:
                tmp_arr = []
                tmp_dict = {}
                temp = data['data']['products'][i]
                url = temp['general']['url_path'] 
                name = temp['general']['name']
                id = temp['general']['product_id']
                manufacturer = temp['general']['manufacturer']
                gia_goc = temp['filterable']['price']
                gia_km = temp['filterable']['special_price']
                tmp_arr += [id, name, manufacturer, gia_goc, gia_km]

                tmp_dict = {
                    'pin': temp['general']['attributes']['battery'],
                    'cam': temp['general']['attributes']['camera_primary'],
                    'chip': temp['general']['attributes']['chipset'],
                    'display': temp['general']['attributes']['display_size'],
                    'type_display': temp['general']['attributes']['mobile_type_of_display'],
                    'sac': temp['general']['attributes']['mobile_cong_nghe_sac'],
                    'storage': temp['general']['attributes']['storage'],   
                }

                url = 'https://cellphones.com.vn/' + url
                tmp_arr += [tmp_dict, url]
                output.append(tmp_arr)
            except Exception as e:
                return f"lỗi: {e}"
        
        return output
    
    def data_to_csv(self, data):
        columns = ['ID', 'Tên', 'Nhà sản xuất', 'Giá gốc', 'Giá khuyến mãi', 'Thông số kỹ thuật', 'URL']
        df = pd.DataFrame(data, columns=columns)
        df.to_csv("data_phone.csv")

# Sử dụng các lớp trong giao diện
obj  = CrawlCellphone()
data = obj.get_list_phone(10)  # Lấy thông tin 10 sản phẩm
info = obj.get_info_phone(data)  
obj.data_to_csv(info)  # Lưu thông tin vào file CSV
