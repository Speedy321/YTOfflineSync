<h2>DISPLAIMER:</h2>
<h3>
This script has been made for my personal use and is available here with no garantee nor anything else.</br>
Feel free to use it as you see fit, but i'm not responsible for anything, not even support or bugfixing.</br>
</br>
This is a basic script that doesn't check for errors nor sanitize it's inputs.</br>
It <b>WILL</b> crash if you do something wrong.</br>
</h3>
</br>
<b>Required python libraries:</b>
- youtube-dl (need to install, installable from pip)
    https://github.com/rg3/youtube-dl/blob/master/README.md
- YoutubeApi (embedded, no need to install)
	"stolen" from https://github.com/rhayun/python-youtube-api
- google, youtube api (? maybe ? probably not)


<b>"api.key" file:</b>
- Generate a api key for YouTube Data API V3 in https://console.developers.google.com/apis/dashboard 
- Copy it into a file called "api.key", in plain text.

<b>"playlists.json" format:</b>

```js
[
    {
        playlist 1 infos
    },
    {
        playlist 2 infos
    }
]
```

<b>Example playlist:</b></br>
<i>Note: If copy-pasting this exemple, remove the comments, json doesn't support comments.</i>

```js
{
  "id": "youtube playlist id",      // The string after list="PLx..." in a youtube url
  "localPath": "path\\to\\folder",  // The absolute path to where you want the videofiles.
									// If using '\' in the path, escape them or crash ('\\')
  "localVersion": 0,                
  "name": "playlist name",          // Local name, doesn't sync with youtube's playlist name.
  "sha1": "autogenerated SHA1 key", // Don't modify unless you want to force update the list.
  "videos": [                       // Autogenerated and used to check for new/deleted videos,

  ],
  "videosNumber": 1
}
```