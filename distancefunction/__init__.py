import pandas
from haversine import haversine
from distancefunction.Event import Event
from datetime import datetime, timedelta


"""Events are object of the class Event. 'threshold' is the (spatial threshold, temporal threshold) applied for distance function.
Note that this threshold may not be the same as the frNN distance threshold applied in spatialkdtree
'distancetype' is a tuple containing at least one of: ('spatial', 'temporal', 'socioeconomic', 'infrastructure') """


def import_data(file, sep):
    df = pandas.read_csv(file, sep=sep)
    return df


def prep_events(df, sociovar_count=0, infravar_count=0):
    events = {}
    for index, row in df.iterrows():
        id = int(row[0])
        lon = float(row[1])
        lat = float(row[2])
        event_date = datetime.strptime(str(int(row[3])), '%Y%m%d')
        population = float(row[4])
        if (sociovar_count + infravar_count) > 0:
            socioeconomic = row[5:(5 + sociovar_count)]
            infrastructure = {}
            infrastructure.update({"proximity": row[4 + sociovar_count + 1: 4 + sociovar_count + 1 + infravar_count]})
            infrastructure.update({"density": row[5 + sociovar_count + infravar_count: 6 + sociovar_count + 2 * infravar_count]})
            e = Event(id, lon, lat, event_date, event_date, population, socioeconomic, infrastructure)
            events.update({id: e})
        else:
            e = Event(id, lon, lat, event_date, event_date, population)
            events.update({id: e})
    return events


def distancefunction(event1, event2, distancetype, threshold):
    dist = {}
    d_spatial = haversine((event1.lat, event1.lon), (event2.lat, event2.lon))
    socioeconomic1, socioeconomic2 = event1.socioeconomic, event2.socioeconomic
    socioeconomic_var_count = event1.get_sociovar_count()
    infrastructure_var_count = event1.get_infravar_count()
    d_socioeconomic = 0
    if event1.socioeconomic is not None:
        for i in range(socioeconomic_var_count):
            # calculating socioeconomic distance with equal weight for each variable
            d_socioeconomic = d_socioeconomic + (abs(socioeconomic1[i] - socioeconomic2[i])/socioeconomic_var_count)
    d_infrastructure = 0
    if event1.infrastructure is not None:
        infra1_proximity, infra1_density = event1.infrastructure["proximity"], event1.infrastructure["density"]
        infra2_proximity, infra2_density = event2.infrastructure["proximity"], event2.infrastructure["density"]
        for i in range(infrastructure_var_count):
            # calculating infrastructure distances with equal weight for each variable
            d_infrastructure = d_infrastructure + \
                               (abs(infra1_proximity[i] - infra2_proximity[i])/(2 * infrastructure_var_count)) + \
                               (abs(infra1_density[i] - infra2_density[i])/(2 * infrastructure_var_count))
    d_spatial_normalized = 0
    if d_spatial >= threshold[0]:
        d_spatial_normalized = 1
    else:
        d_spatial_normalized = d_spatial/threshold[0]

    main_event = None
    second_event = None
    if event1.event_date < event2.event_date:
        main_event = event1
        second_event = event2
    elif event1.event_date > event2.event_date:
        main_event = event2
        second_event = event1
    elif event1.event_date == event2.event_date:
        if event1.population > event2.population:
            main_event = event1
            second_event = event2
        else:
            main_event = event2
            second_event = event1

    d_temporal_directional = 0
    if main_event.event_date == main_event.end_date:
        delta = second_event.event_date - main_event.end_date
        d_temporal_directional = delta.days
    else:
        delta1 = second_event.event_date - main_event.end_date
        delta2 = main_event.end_date - main_event.event_date
        d_temporal_directional = delta1.days / delta2.days

    if d_temporal_directional >= threshold[1]:
        d_temporal_normalized = 1
    else:
        d_temporal_normalized = d_temporal_directional / threshold[1]

    dist.update({'spatial': d_spatial_normalized, 'temporal': d_temporal_normalized, 'infrastructure':d_infrastructure,
              'socioeconomic': d_socioeconomic})

    wt_temporal = main_event.population / (main_event.population + second_event.population + 1)
    wt_spatial = 1 - wt_temporal
    d_spatiotemporal = 0
    # distances = 1
    # d_final = 0
    if 'spatial' in distancetype and 'temporal' in distancetype:
        d_spatiotemporal = (d_spatial_normalized * wt_spatial) + (d_temporal_normalized * wt_temporal)
        dist.update({'spatiotemporal': d_spatiotemporal})
        dist.pop('spatial')
        dist.pop('temporal')
        # distances = len(distancetype) - 1
        # d_final = d_spatiotemporal / distances
        # if 'socioeconomic' in distancetype:
        #     d_final = d_final + (dist["socioeconomic"] / distances)
        # if 'infrastructure' in distancetype:
        #     d_final = d_final + (dist["infrastructure"] / distances)
    # else:
    #     distances = len(distancetype)
    #     if 'spatial' in distancetype:
    #         d_final = d_final + (dist["spatial"] / distances)
    #     if 'temporal' in distancetype:
    #         d_final = d_final + (dist["temporal"] / distances)
    #     if 'socioeconomic' in distancetype:
    #         d_final = d_final + (dist["socioeconomic"] / distances)
    #     if 'infrastructure' in distancetype:
    #         d_final = d_final + (dist["infrastructure"] / distances)
    return dist




