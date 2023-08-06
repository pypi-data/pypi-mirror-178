# Changelog

<!--next-version-placeholder-->

## v0.21.1 (2022-11-24)
### Fix
* Matplotlib fig.canvas.set_window_title() deprecated in Matplotlib>=3.4 ([`6459d5f`](https://github.com/Sieboldianus/TagMaps/commit/6459d5f8ee4395677fa3d1eedf6d8dda8fd40eda))
* EMOJI_UNICODE deprecated in emoji>=2.0.0 ([`9d1e243`](https://github.com/Sieboldianus/TagMaps/commit/9d1e2438ce81cbf8e65f3d47fad3c17afbcfbd61))

### Documentation
* Add comparison graphic for Mapnik/ArcPro rendering ([`e15682d`](https://github.com/Sieboldianus/TagMaps/commit/e15682d2626d883f9997b9121705789da91fcb1c))

## v0.21.0 (2022-07-27)
### Feature
* Add export to Mapnik ([`9db0d0d`](https://github.com/Sieboldianus/TagMaps/commit/9db0d0dc0a266f9eef7c3aac5bf663337c096f80))

### Documentation
* Add section on visualization with Mapnik ([`25dbb2c`](https://github.com/Sieboldianus/TagMaps/commit/25dbb2c0208f42d844fe92d6c863f909ce395f4f))
* Add webm link to animation ([`f1190c8`](https://github.com/Sieboldianus/TagMaps/commit/f1190c8521851d93a13d3227ec031b51928c59fe))
* Add label placement animation ([`82c987d`](https://github.com/Sieboldianus/TagMaps/commit/82c987d3af76b9c7343d5088adc8c1ae587e3b6d))
* Remove deprecated cx_freeze references ([`92098e6`](https://github.com/Sieboldianus/TagMaps/commit/92098e6bd7d2817ca2c537401d3a19b9dc1dacbf))
* Add publication link ([`9e3cb16`](https://github.com/Sieboldianus/TagMaps/commit/9e3cb163123ebbc87207d9ad56a6e457ac3fd28a))
* Improve readme for resource folder ([`f8ef9f7`](https://github.com/Sieboldianus/TagMaps/commit/f8ef9f746d5cb0bfe14022c182f3c06e8fbb1040))
* Add note to resources folder ([`ff9fe96`](https://github.com/Sieboldianus/TagMaps/commit/ff9fe962acbb2c833551e218137cab683e04fbcd))

## v0.20.12 (2022-01-19)
### Fix
* ShapelyDeprecationWarning use geoms property ([`1352ea9`](https://github.com/Sieboldianus/TagMaps/commit/1352ea94feb77db37b5305a9f6281e5c5b2834b5))

## v0.20.11 (2022-01-18)
### Fix
* Deprecated shapely cascaded_union() ([`2dfb2a1`](https://github.com/Sieboldianus/TagMaps/commit/2dfb2a13ddc544b7cf78fffc9b7f47d4788b9678))

### Documentation
* Add git revision date to pages ([`728dcd4`](https://github.com/Sieboldianus/TagMaps/commit/728dcd4fcaa17622259901b1477a8ff505889e30))
* Improve formatting and revise structure ([`c1d1cc0`](https://github.com/Sieboldianus/TagMaps/commit/c1d1cc04a97dbe49ad2cd85f12efc71db778ca89))
* Cleanup changelog ([`9ce4021`](https://github.com/Sieboldianus/TagMaps/commit/9ce40210cfe42620f1d99aaad687e37984c34f19))

## v0.20.10 (2021-02-18)
### Fix
* Graphemes not found in newest emoji.UNICODE_EMOJI (emoji >= v.1.0.1) ([`9952cd2`](https://github.com/Sieboldianus/TagMaps/commit/9952cd253d3637d8dff1304541720e9f37ea1abd))

### Documentation
* Correct order of pip --editable --no-deps ([`5c58cdd`](https://github.com/Sieboldianus/TagMaps/commit/5c58cdda327191796a0e37f9388ca0605b6dac75))

## v0.20.9 (2021-01-03)
### Fix
* Correct pin joblib ([`7c87979`](https://github.com/Sieboldianus/TagMaps/commit/7c879795975f7c3e54ce9088418f7dfc12b9e5c4))

## v0.20.7 (2021-01-03)
### Fix
* Name not found on manual get_cluster_shapes_map() ([`6bd9d66`](https://github.com/Sieboldianus/TagMaps/commit/6bd9d665eabfce7ed6bb3dfe7f7549df61ee9dfb))

### Documentation
* Add pip --editable note ([`c51d75a`](https://github.com/Sieboldianus/TagMaps/commit/c51d75aaa55e341e6a074fe01977a0504364da53))

## v0.20.5 (2021-01-03)
### Fix
* Emoji flags split from grapheme clusters ([`c0512e3`](https://github.com/Sieboldianus/TagMaps/commit/c0512e33a11af0d4ef026b12453bff65954f1f85))
* Move from ThreadPool to threading.Thread/Queue, related to joblib freeze issue 1002 (see below) ([`23995e2`](https://github.com/Sieboldianus/TagMaps/commit/23995e27d9d5b2382fb184cdeb074d7f80bf284f))

### Documentation
* Minor rephrase of introduction ([`6f6ddfc`](https://github.com/Sieboldianus/TagMaps/commit/6f6ddfc45c6174a90ef90abaf8c902119cb1921a))
* Add super-submodule docstrings ([`2e98868`](https://github.com/Sieboldianus/TagMaps/commit/2e98868dd1a85fa2aafffdf9bd906a8aff8cc8da))
* Update about section ([`d5c7878`](https://github.com/Sieboldianus/TagMaps/commit/d5c7878b47dc651f891e960a9758dd5e9a9ac59a))
* Update Linux install instructions ([`cf023dc`](https://github.com/Sieboldianus/TagMaps/commit/cf023dc0772cfb22630f38668ddce90be7d254cc))
* Enable API docs for __main__ ([`518b205`](https://github.com/Sieboldianus/TagMaps/commit/518b20551a29cdfb17f6e0ee7f8475866eb02800))
* Fix readme download link ([`1ff63ae`](https://github.com/Sieboldianus/TagMaps/commit/1ff63ae546f552cae5c559a76cb4adbf3f833dc4))
* Update release notes, add link to win-37 build ([`f224de2`](https://github.com/Sieboldianus/TagMaps/commit/f224de20d0d3e68a67c4d48443432ddf31893f5a))
* Update release notes, add link to win-37 build ([`5bfcc76`](https://github.com/Sieboldianus/TagMaps/commit/5bfcc76dafd9786fc7b7b66cc06a7313db3269f2))
