import http.client
class Company:
    def CompanyInformation(self,index1):
        conn = http.client.HTTPSConnection("crunchbase-crunchbase-v1.p.rapidapi.com")

        headers = {
            'X-RapidAPI-Host': "crunchbase-crunchbase-v1.p.rapidapi.com",
            'X-RapidAPI-Key': "c5203d15d3msha0a51d8d944d3d7p10fe07jsnad57cba7aa0a"
            }
        # index1 = "acer"
        conn.request("GET", "/autocompletes?query={}".format(index1), headers=headers)

        res = conn.getresponse()
        data = res.read()
        x = data.decode("utf-8")
        spl_word = "}"
        #print(data.decode("utf-8"))
        try:
            y = x.split(f'short_description":',1)[1]
            res = y.partition(spl_word)[0]
        except IndexError:
            res = 'No information found'

        return res
