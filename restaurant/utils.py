

def get_restaur_info(restaurant):
    return {"name": restaurant.name,
            "description": restaurant.description,
            }


def restaurant_place_info(restaurant):
    return {"work_from": restaurant.work_from,
            "work_to": restaurant.work_to,
            "address": {"longitude": restaurant.longitude, "latitude": restaurant.latitude},
            }
