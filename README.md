# 覚えておいてほしい単語

- `offset` ... 位置。多くの場合 x,y

- `size` ... 大きさ。多くの場合 w,h

  - `w`, `width` ... 横幅
  - `h`, `height` ... 縦幅

- `rect` ... 四角

  - `l`, `left` 左
  - `t`, `top` 上
  - `r`, `right` 右
  - `b`, `right` 下

- `Length` ... 長さを表す。int か float で指定する。

# ユーティリティ概要

- `Offset`, `Size`, `Rect` ... レイアウト関係のクラス。
- `Color` ... 色関係のクラス。

# docker

## build

```
docker buildx build --platform linux/amd64 -t asia.gcr.io/megane-s-gcp/minshumi-image-gen .
```

## push

```
docker push asia.gcr.io/megane-s-gcp/minshumi-image-gen
```
