import openaq
import json
api = openaq.OpenAQ()


# api pull data call
status, body = api.measurements(city='Los Angeles', parameter='pm25')
results = body['results']
data = []
for result in results:
    date = result['date']['utc']
    value = result['value']
    data.append((date, value))

# for getting a record into the database
for date, value in data:
    record = (date, value)
    # print(record)

# stretch goal, implement another pull request
status, resp = api.cities()
results = resp['results']
# print(results)
# x = results.get("city")
# y = results.get("count")
# print([x, y])

data = []
status, resp = api.cities()
results = resp['results']
for result in results:
    city = result["city"]
    count = result["count"]
    data.append((city, count))
print(data)


