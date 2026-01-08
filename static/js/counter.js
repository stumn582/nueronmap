function animateCounter(id, target) {
    let count = 0;
    const el = document.getElementById(id);
    const step = target / 50;

    const interval = setInterval(() => {
        count += step;
        if (count >= target) {
            el.innerText = target;
            clearInterval(interval);
        } else {
            el.innerText = Math.floor(count);
        }
    }, 20);
}

