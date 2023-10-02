import joblib
import json
import argparse
import numpy as np
import spotipy
import scipy


def arg_parse():
    parser = argparse.ArgumentParser(description='쏜못넬스텐의 노래 중 가장 비슷한 노래를 추천해 줍니다.')
    parser.add_argument('--clientid', type=str, help='Spotify API Client ID')
    parser.add_argument('--clientsecret', type=str, help='Spotify API Client Secret')
    parser.add_argument('-uri', type=str,  help='Spotify Song URI')
    args = parser.parse_args()
    return args


def get_song(uri: str, client_id: str, client_secret: str) -> list:
    model = joblib.load('classification_model.pkl')
    with open('song_distributions.json', 'r', encoding='utf-8-sig') as f:
        songs = json.load(f)

    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id=client_id,
                                                                         client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    d = sp.audio_features(uri)[0]
    features=[d['acousticness'], d['danceability'], d['energy'], d['valence']]
    prob = model.predict_proba(np.array(features).reshape(-1, 4))[0].tolist()

    song_lists = [[None, 1e10, "쏜애플"], [None, 1e10, "국카스텐"], [None, 1e10, "넬"], [None, 1e10, "못"]]
    cnt = 0
    for i in songs.keys():
        temp = sum(scipy.special.rel_entr(prob, songs[i]))
        if cnt <= 40:
            idx = 0
        elif cnt <= 91:
            idx = 1
        elif cnt <= 141:
            idx = 2
        else:
            idx = 3
        cnt += 1
        if song_lists[idx][1] > temp:
            song_lists[idx][0] = i
            song_lists[idx][1] = temp

    return song_lists


def main():
    args = arg_parse()
    print(get_song(args.clientid, args.clientsecret, args.uri))


if __name__ == '__main__':
    main()