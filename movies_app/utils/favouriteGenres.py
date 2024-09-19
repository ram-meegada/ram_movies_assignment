from movies_app.models import MoviesCollectionModel, MoviesModel

def get_favourite_genres(collection_ids):
    try:
        movie_ids = MoviesCollectionModel.objects.filter(collection__in=collection_ids).values_list('movie', flat=True)
        geners = MoviesModel.objects.filter(id__in=movie_ids).values_list('genres', flat=True)
        all_geners = ",".join(list(geners))
        temp = {}
        for i in all_geners.split(","):
            if not i:
                continue
            if i not in temp:
                temp[i] = 1
            else:
                temp[i] += 1
        sorted_geners = sorted(temp.items(), key=lambda v: v[1], reverse=True)
        return ", ".join(list(map(lambda v: v[0], sorted_geners[:3])))
    except Exception as err:
        return str(err)