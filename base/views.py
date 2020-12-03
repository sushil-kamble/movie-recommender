import base64
import difflib
import urllib

import pandas as pd
import numpy as np
import io
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from users.forms import UserRegisterForm
from users.models import Watchlist

sheet_id = '147W5MrCDKw7CHhvRZqKq6XoXAp_CPav5rcXveyUAlFc'
df = pd.read_csv(
    f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
pd.set_option('display.max_colwidth', None)
dfList = df.values.tolist()
dfTop = df.sort_values(by='rating', ascending=False)[0:100]
dfTopList = dfTop.values.tolist()


def register(request):
    if request.user.is_authenticated:
        return redirect('mainPage')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def watchList(request):
    movie = request.POST.get('movie')
    user_title_watchlist = list(
        [x.movie for x in Watchlist.objects.filter(author=request.user)])
    if request.method == 'POST':
        if movie[:6] != "deletE":
            if movie not in user_title_watchlist:
                addMovie = Watchlist(movie=movie, author=request.user)
                messages.success(
                    request, f'{movie} Successfully added to your Watchlist')
                addMovie.save()
                return redirect('watchlist')
            else:
                messages.info(
                    request, f'{movie} was already present in your Watchlist')
                return redirect('watchlist')
        else:
            deleteMovie = Watchlist.objects.filter(
                movie=movie[6:], author=request.user)
            messages.error(
                request, f'{movie[6:]} has been Deleted')
            deleteMovie.delete()
            return redirect('watchlist')
    df_user_watchlist = df.set_index(
        'title').loc[user_title_watchlist].reset_index(inplace=False)
    list_user_watchlist = df_user_watchlist.values.tolist()[::-1]
    return render(request, 'watchlist.html', {'list_user_watchlist': list_user_watchlist})


def convert_into_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return urllib.parse.quote(string)


def rating_number():
    plt.figure(figsize=(12, 10))
    plt.bar(df['rating'], df['noOfRating'] / max(df['noOfRating']), color='#FFBB33')
    plt.xlabel('IMDB Rating')
    plt.ylabel('Normalized No of Rating')
    plt.title('Rating vs Normalized No of Rating')
    plt.margins(0.1)
    plt.subplots_adjust(bottom=0.28)
    plt.tight_layout()
    plt.plot()
    fig = plt.gcf()
    return convert_into_base64(fig)


def genre_graph(categories, by, labelx, labely, title):
    plt.figure(figsize=(12, 10))
    genre_list = []
    for cat in sorted(categories):
        genre_list.append(np.average(df[df["genre"].str.contains(cat)][by]))
    plt.bar(sorted(categories), [x / max(genre_list) for x in genre_list], color="#FFBB33")
    plt.xticks(rotation=90)
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.title(title)
    plt.margins(0.1)
    plt.subplots_adjust(bottom=0.28)
    plt.tight_layout()
    plt.plot()
    fig = plt.gcf()
    return convert_into_base64(fig)


def year_rating():
    years = np.arange(2000, 2021, 1)
    yrRat = []
    for year in years:
        yrRat.append(np.mean(df[df['year'] == year]['rating']))
    plt.figure(figsize=(12, 10))
    plt.bar(years, yrRat, color='#FFBB33')
    plt.xlabel('Years')
    plt.ylabel('Average IMDB Rating')
    plt.title('Years vs Average IMDB Rating')
    plt.tight_layout()
    plt.plot()
    fig = plt.gcf()
    return convert_into_base64(fig)


def pie_number(categories):
    colors = ['blue', 'red', 'orange', 'grey', 'purple', '#AD1457', '#1A237E', '#BF360C', '#006064', '#33691E', '#263238']
    aggCat = []
    plt.figure(figsize=(12, 10))
    for cat in sorted(categories):
        aggCat.append(np.mean(df[df["genre"].str.contains(cat)]['noOfRating']))
    plt.pie(aggCat, labels=categories, colors=colors, wedgeprops={'edgecolor': '#FFBB33'}, autopct='%1.1f%%')
    plt.title('PIE: Average Normalized Number of Rating')
    plt.tight_layout()
    plt.plot()
    fig = plt.gcf()
    return convert_into_base64(fig)


def hist_number():
    plt.figure(figsize=(12, 10))
    plt.hist(df['rating'], bins=20, edgecolor='black', color='#FFBB33')
    plt.xlabel('IMDB Rating')
    plt.ylabel('Number of movies')
    plt.title('HISTOGRAM: IMDB Rating vs Number of movies')
    plt.tight_layout()
    plt.grid(False)
    plt.plot()
    fig = plt.gcf()
    return convert_into_base64(fig)


def home(request):
    # TODO: GRAPHS
    plt.style.use("dark_background")
    categories = ['Drama', 'Horror', 'Action', 'Animation', 'Sci-Fi', 'Comedy',
                  'Thriller', 'Adventure', 'Family', 'Mystery', 'Crime']
    genGraph1 = genre_graph(categories, 'noOfRating', 'Genre', 'Average Normalized Rating',
                            'Genre vs Average Normalized Number of Rating')
    genGraph2 = genre_graph(categories, 'rating', 'Genre', 'IMDB rating',
                            'Genre vs IMDB rating')

    return render(request, "home.html", {'graph1': rating_number(), 'graph2': genGraph1, 'graph3': genGraph2,
                                         'graph4': year_rating(), 'graph5': pie_number(categories),
                                         'graph6': hist_number()})


def mainPage(request):
    return render(request, "mainPage.html", {'movieList': dfList})


def allPage(request):
    return render(request, "all.html", {'dfList': dfList})


def allSeries(request):
    dfSeries = df[df['_type'] == "Series"].values.tolist()
    return render(request, "series.html", {'movieList': dfSeries})


def topPage(request):
    return render(request, "top100_page.html", {'movieList': dfTopList})


def advSearchResults(request):
    dfAdv = df.copy()
    allStars = list(set([j for sub in list(df['stars'].str[2:-2].str.replace("'", "")
                                           .str.replace('"', '').str.split(', ')) for j in sub]))
    if request.method == 'GET':
        getImdb = request.GET.get('getimdb')
        getYear = request.GET.get('getyear')
        getStar = request.GET.get('getStar')
        getKeywords = request.GET.get('getKeywords')
        getGenre = request.GET.get('getgenre')
        sorting = request.GET.get('inlineDefaultRadios')
        getStar = difflib.get_close_matches(getStar, allStars)
        if len(getStar) > 0:
            getStar = getStar[0]
        else:
            getStar = ""
        if getGenre == "All":
            getGenre = ""
        if not getYear:
            getYear = 0
        if not getImdb:
            getImdb = 0.0
        if sorting == "byyear":
            dfSelect = dfAdv[(dfAdv['rating'] >= float(getImdb)) & (dfAdv['year'] >= int(getYear)) &
                             (dfAdv["genre"].str.contains(getGenre, na=False)) &
                             (dfAdv["stars"].str.contains(getStar, na=False)) &
                             (dfAdv["keywords"].str.contains(getKeywords, na=False))].sort_values(by='year',
                                                                                                  ascending=False)
        else:
            dfSelect = dfAdv[(dfAdv['rating'] >= float(getImdb)) & (dfAdv['year'] >= int(getYear)) &
                             (dfAdv["genre"].str.contains(getGenre, na=False)) &
                             (dfAdv["stars"].str.contains(getStar, na=False)) &
                             (dfAdv["keywords"].str.contains(getKeywords, na=False))].sort_values(by='rating',
                                                                                                  ascending=False)
        dfSelect = dfSelect.values.tolist()
        if getGenre == "":
            getGenre = "All"
        if getStar == "":
            getStar = "All"
        if getKeywords == "":
            getKeywords = "Any"
        if sorting == "byyear":
            sorting = "By Year"
        else:
            sorting = "By Imdb"
        return render(request, "advSearchResults.html", {'movieList': dfSelect, 'movieLen': len(dfSelect),
                                                         'getimdb': getImdb, 'getyear': getYear, 'getgenre': getGenre,
                                                         'getStar': getStar, 'getKeywords': getKeywords,
                                                         'sorting': sorting})
    else:
        return render(request, "advSearchResults.html")


def genrePage(request):
    genre_type = request.GET.get('typeGenre', "False")
    if genre_type == "Netflix":
        df1 = df.copy()
        df1 = df1[df1['netflix'].notna()]
        dfTopNet = df1.sort_values(by='rating', ascending=False)
        genre = dfTopNet.values.tolist()
        return render(request, "genre.html", {'movieList': genre, 'genre_type': genre_type})
    genre = []
    for i in range(0, len(df)):
        if genre_type in df["genre"][i]:
            genre.append(df.iloc[i].values.tolist())
    dfByGenre = pd.DataFrame(genre,
                             columns=['imdbno', 'title', 'rating', 'link', 'noOfRating', 'genre', 'stars', 'runtime',
                                      '_type', 'netflix', 'desp', 'keywords', 'year', 'coverUrl'])
    dfTopGenre = dfByGenre.sort_values(by='rating', ascending=False)
    genre = dfTopGenre.values.tolist()
    return render(request, "genre.html", {'movieList': genre, 'genre_type': genre_type})


def result_page(request):
    movie = request.POST.get('movie', "False")
    search = df[df['title'] == movie]
    imdbNo = search['imdbno'].to_string(index=False).strip()
    title = search['title'].to_string(index=False).strip()
    rating = search['rating'].to_string(index=False).strip()
    link = search['link'].to_string(index=False).strip()
    # noOfRating = search['noOfRating'].to_string(index=False).strip()
    genre = search['genre'].to_string(index=False).strip()
    genreOneByOne = genre.split(',')
    stars = search['stars'].to_string(index=False).strip()
    starsList = stars[2:-2].replace("'", "").split(',')
    runtime = search['runtime'].to_string(index=False).strip()
    mType = search['_type'].to_string(index=False).strip()
    netflix = search['netflix'].to_string(index=False).strip()
    description = search['desp'].to_string(index=False).strip()
    soup = BeautifulSoup(requests.get(link).text, "html.parser")
    raw = soup.find("link", {'rel': 'image_src'})
    img_imdb = raw.get("href")
    noOfRating = soup.find("span", {"class": "small"}).get_text()
    resultPageVar = {'movie': movie, 'imdbno': imdbNo, 'title': title,
                     'rating': rating, 'link': link, 'noOfRating': noOfRating, 'genre': genre,
                     'stars': stars, 'runtime': runtime, 'mtype': mType, 'desp': description,
                     'netflix': netflix, 'genreonebyone': genreOneByOne,
                     'starsList': starsList, 'img_imdb': img_imdb}
    if df[df['imdbno'] == imdbNo]['netflix'].to_string(index=False).strip() != "NaN":
        back = True
        soup = BeautifulSoup(requests.get(netflix).text, "html.parser")
        raw = soup.find("div", {'class': 'hero-image hero-image-desktop'})
        try:
            background = raw.get('style')[35:-2]
            logo = soup.find("img", {'class': 'logo'}).get('src')
            return render(request, "result.html", {'movie': movie, 'imdbno': imdbNo, 'title': title,
                                                   'rating': rating, 'link': link, 'noOfRating': noOfRating,
                                                   'genre': genre, 'stars': stars, 'runtime': runtime,
                                                   'mtype': mType, 'desp': description,
                                                   'netflix': netflix, 'background': background, 'back': back,
                                                   'genreonebyone': genreOneByOne, 'starsList': starsList,
                                                   'img_imdb': img_imdb, 'logo': logo})
        except:
            return render(request, "result.html", resultPageVar)
    return render(request, "result.html", resultPageVar)
