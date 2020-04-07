function pageGoTo(page) {
    let url = location.href;
    if (url.indexOf('?') < 0){ url += '?' }

    url = `${url}&page=${this.page}`;
    location.href = url;
}
