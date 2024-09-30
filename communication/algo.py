from typing import List, TypedDict
import requests

# URL of the FastAPI endpoint
LOCALHOST_URL = "http://192.168.32.26:8000"
ALGO_URL = "/algo/live"

class Obstacle(TypedDict):
    id: int
    x: int
    y: int
    d: int

class Value(TypedDict):
    obstacles: List[Obstacle]

class RequestBody(TypedDict):
    cat: str
    value: Value
    server_mode: str
    algo_type: str

# SAMPLE OBSTACLES ARRAY:
# [
#   { "id": 1, "x": 15, "y": 10, "d": 4 }, # 10cm grid (x, y)
#   { "id": 2, "x": 1, "y": 18, "d": 2 }, # 10cm grid (x, y)
# ],

def get_stm_commands(obstacles: List[Obstacle]):
    print("Obstacles from android: ", obstacles)
    request_body: RequestBody = {
      "cat": "obstacles",
      "value": {
        "obstacles": obstacles
      },
      "server_mode": "live",
      "algo_type": "Exhaustive Astar"
    } 
    response = requests.post(LOCALHOST_URL+ALGO_URL, json=request_body)
    print('Status of request:', response.status_code)
    print('Response:', response.json())
    return response.json()

#uncomment to test endpoint
# if __name__ == "__main__":
#     obstacles = [
#         { "id": 1, "x": 15, "y": 10, "d": 4 },
#         { "id": 2, "x": 1, "y": 18, "d": 2 },
#     ]
#     commands_object_json = get_stm_commands(obstacles)
#     print('Commands object json:', commands_object_json)
