# auto-cpufreq-genAI-chatbot

I built [auto-cpufreq](https://github.com/AdnanHodzic/auto-cpufreq/) genAI chatbot to handle support, answer questions, and assist with its installation and configuration, since open-source project grew too popular to manage manually. So in the process I essentially automated myself as part of:

- Blog post: [How I replaced myself with a GenAI chatbot using Gemini](https://foolcontrol.org/?p=4903)  
- Youtube video: [How I replaced myself with a GenAI chatbot using Gemini](https://www.youtube.com/watch?v=a-UcwAAXOoc)

The idea is that you follow along in what's described in [From Zero to AI Hero: How to Build a GenAI Chatbot with Gemini & Vertex AI Agent Builder](https://foolcontrol.org/?p=5051) blog post and/or [(17 video) Youtube video playlist](https://www.youtube.com/watch?list=PL83G0TLSeXRFiTPyctEn_vdL2_Z7xd-e_&v=LgAUPJm4Dio). Which expands on what I said before as part of my initial blog post/Youtube video, build the same chatbot I did, and then customize it with your own data to fit your unique GenAI chatbot use case.

This repository contains Python scripts to fetch its data from GitHub, YouTube, and Reddit APIs, which is then fed into the chatbot’s data store and used as part of a Retrieval-Augmented Generation (RAG) workflow.

auto-cpufreq genAI chatbot is built on Google Cloud, and leverages Vertex AI Agent Builder and Conversational Agents, powered by the Gemini LLM.

_From Zero to AI Hero: How to Build a GenAI Chatbot with Gemini & Vertex AI Agent Builder Youtube playlist:_

[![From Zero to AI Hero: How to Build a GenAI Chatbot with Gemini & Vertex AI Agent Builder (17 video) YouTube playlist](https://img.youtube.com/vi/LgAUPJm4Dio/0.jpg)](https://www.youtube.com/watch?v=LgAUPJm4Dio&list=PL83G0TLSeXRFiTPyctEn_vdL2_Z7xd-e_)


### Create API keys needed to fetch data from Github, Youtube & Reddit

#### Prerequisites before "Data Fetch" Python Scripts can be run

Ensure you have the necessary API keys for GitHub, YouTube, and Reddit by following instructions below.

#### Github

Create [Github Personal access tokens under Developer Settings](https://github.com/settings/apps)

I went with [Token (classic)](https://github.com/settings/apps) and gave it full access to repo section and select: "Full control of private repositories"

<img src="https://storage.googleapis.com/foolcontrol-media/2025/02/e0ae6e03-create-github-personal-access-token.png" alt="How to create Github personal access token" width="800px">

#### Youtube

1. Enable ["YouTube Data API v3" in Google Cloud Console](https://console.cloud.google.com/apis/api/youtube.googleapis.com/credentials?inv=1&invt=AboxZg&project)
2. Under "Create credentials", create "Youtube API" key
3. Click on "Youtube API" to set key restrictions, e.g: "Youtube Data API v3" so only this API can use it (or that it can only be used from your IP).

<img src="https://storage.googleapis.com/foolcontrol-media/2025/02/8a87d09a-restrict-youtube-api-key.png" alt="How to restrict Youtube API key" width="800px">

#### Reddit

Click on ["Create app" in Reddit "apps ("developed applications")](https://www.reddit.com/prefs/apps/)

### Copy API secrets to your terminal configuration file

In case you use Zsh, e.g: `vim ~/.zshrc`


```
# auto-cpufreq genAI chatbot API keys
# reference: https://github.com/AdnanHodzic/auto-cpufreq-genAI-chatbot
                                                                                                                                                        
# github token
export github_export_token="REDACTED

# reddit
export reddit_client_id="REDACTED"
export reddit_client_secret="REDACTED"

# Youtube API key
export youtube_api_key="REDACTED"
```

Followed by: `source ~/.zshrc`

### How to run "Data fetch" Python scripts

_How to fetch data from defined GenAI Chatbot Data Sources:_

[![How to fetch data from defined GenAI Chatbot Data Sources"](https://img.youtube.com/vi/N3i-8hYHfTo/0.jpg)](https://www.youtube.com/watch?v=N3i-8hYHfTo)


Since all requirements to run any of the .py files are stored in a single [Pipfile](#Pipfile) file, after you have [pipenv](https://pipenv.pypa.io/en/latest/installation.html)  installed on your system, you'll need to run `pipenv install` the first time to install needed dependencies.

After which you can run each script with:

#### Github 

* github_export_**readme**.py - `pipenv run python github_export_readme.py`
* github_export_**issues**.py - `pipenv run python github_export_issues.py`
* github_export_**discussions**.py - `pipenv run python github_export_discussions.py`
* github_export_**pull_requests**.py - `pipenv run python github_export_pull_requests.py`
* github_export_**releases**.py - `pipenv run python github_export_releases.py $URL`

#### Youtube

* youtube_**transcript**_downloader.py - `pipenv run python youtube_transcript_downloader.py $URL`
* youtube_**comments**_downloader.py - `pipenv run python youtube_comments_downloader.py $URL`

#### Reddit

* reddit_**post_comments**_export.py - `pipenv run python reddit_post_comments_export.py $URL`

The exported HTML files, containing all necessary data, will be stored in the Data/ directory, organized by source.
