; ============================================================
; ミラの未来視 - EPISODE 1
; CHAPTER 1 ：「ノイズとの遭遇」
; ============================================================

*chapter01_start

; --- 背景：学校付近の街 （朝） ---
[bg storage="bg_street_morning.jpg" time=1500]
[bgm storage="bgm_daily.mp3" loop=true volume=70]
[fadein time=1000]

[chara_show name="you" storage="chara_you_normal.png" pos="left" time=500]
[cm]

　ある朝。いつもと変わらない、ただの朝のはずだった。[p]

ヨウ「（……なんか視線感じる）」[p]

[chara_show name="mira" storage="chara_mira_normal.png" pos="right" time=500]

[chara_face name="you" face="surprised"]
ヨウ「……誰？」[p]

[chara_face name="mira" face="normal"]
ミラ「ミラです。【個体識別番号：M-01】。あなたの未来を観測しています」[p]

[chara_face name="you" face="flat"]
ヨウ「……へぇ」[p]

[chara_face name="mira" face="thinking"]
ミラ「驚かないんですか」[p]

[chara_face name="you" face="flat"]
ヨウ「驚く体力がない」[p]

[chara_face name="mira" face="blink"]
ミラ「……予測外の回答です」[p]

[cm]
　こうして、最適解をぶち壊すノイズと、[l]
計算外の出来事ばかり見る未来視AIの、[l]
奇妙な日常が始まった。[p]

; --- 第一話終了・次話へ ---
[fadeout time=1500]
[jump storage="ep01_chapter02.ks" target="*chapter02_start"]
