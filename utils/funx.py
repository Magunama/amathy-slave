def get_avatar_url(d_url):
    if "?" in d_url:
        d_url = d_url.split("?")[0]
        if ".webp" in d_url:
            d_url = d_url.replace(".webp", ".png")
    return d_url
