Required python libraries:
- youtube-dl 
    https://github.com/rg3/youtube-dl/blob/master/README.md
- YoutubeApi (embedded, no need to install)
	"stolen" from https://github.com/rhayun/python-youtube-api
- google, youtube api (? maybe ? probably not)


"api.key" file:
- Generate a api key for YouTube Data API V3 in https://console.developers.google.com/apis/dashboard 
- Copy it into "api.key" in plain text.

"playlists.json" format:
[
    {
        playlist 1 infos
    },
    {
        playlist 2 infos
    }
]

Example playlist:
//If copy-pasting this exemple, remove the comments, json doesn't support comments.
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