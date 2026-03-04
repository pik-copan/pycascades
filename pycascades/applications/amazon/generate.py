from core.system.system import network
from .amazon import amazon_double_well

NUMBER_OF_CELLS = 416


def construct_amazon(
    historical_data,
    current_data,
    links,
    coordinates,
    mean_data
):
    cells = [
        amazon_double_well(
            map       = current_data["map"][i],
            mcwd      = current_data["mcwd"][i],
            map_crit  = historical_data["map_crit"][i],
            mcwd_crit = historical_data["mcwd_crit"][i],
            map_mean  = mean_data["map"][i],
            mcwd_mean = mean_data["mcwd"][i],
        ) for i in range(NUMBER_OF_CELLS)
    ]

    amazon = network()
    for cell in cells:
        amazon.add_element(cell)

    for i in range(NUMBER_OF_CELLS):
        amazon.nodes[i]['pos'] = (coordinates["lon"][i], coordinates["lat"][i])

    #for idx, val in enumerate(np.transpose(links["delta_map"])):
    #    if (val[2] > 1 or links["delta_mcwd"][2, idx] > 0.1):
    #        amazon.add_coupling(
    #            from_id = int(val[1]),
    #            to_id = int(val[0]),
    #            coupling = amazon_coupling(
    #                delta_map  = val[2],
    #                delta_mcwd = links["delta_mcwd"][2, idx],
    #                map        = current_data["map"][int(val[0])],
    #                mcwd       = current_data["mcwd"][int(val[0])],
    #                map_crit   = historical_data["map_crit"][int(val[0])],
    #                mcwd_crit  = historical_data["mcwd_crit"][int(val[0])],
    #                map_mean   = mean_data["map"][int(val[0])],
    #                mcwd_mean  = mean_data["mcwd"][int(val[0])],
    #                x_0        = -1.0
    #            )
    #        )
    for x_val in range(NUMBER_OF_CELLS):
       for y_val in range(NUMBER_OF_CELLS):
           if (links["delta_map"][x_val][y_val] > 1 or links["delta_mcwd"][x_val][y_val] > 0.1) and x_val != y_val:
               amazon.add_coupling(
                   from_id = y_val,
                   to_id = x_val,
                   coupling = amazon_coupling(
                       delta_map  = links["delta_map"][x_val][y_val],
                       delta_mcwd = links["delta_mcwd"][x_val][y_val],
                       map        = current_data["map"][x_val],
                       mcwd       = current_data["mcwd"][x_val],
                       map_crit   = historical_data["map_crit"][x_val],
                       mcwd_crit  = historical_data["mcwd_crit"][x_val],
                       map_mean   = mean_data["map"][x_val],
                       mcwd_mean  = mean_data["mcwd"][x_val],
                       x_0        = -1.0
                   )
               )
    return amazon
