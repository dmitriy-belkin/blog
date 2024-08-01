document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('theme-toggle');
    const darkThemeClass = 'dark-theme';
    const lightIcon = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACQAAAA8CAYAAAAOhRhuAAABdklEQVRoQ+1XMWrDQBCUf6EHqAyYgPyCOGV6PUPgQNADEhOIQVWqPEBdipR2XmBBMLhU6UKQRyQEUnhO5kaLBLLMqFt29zQ3O7d3Own498NDTBETX7TX+Z8oQIzvwRkCAM/LJQC+mc/ZBsD/udmA/ZBlbj7I5pSGBOiYsvExlCQJ1LwoCpOGWuTbNNRiQS/AFvkCxEreO0PuwYC2MUTJBMikgSAIBi+Zjj0r2eUzBCIst1vY8ctqBXYYhqa7rK5riL9fLMCOZzOw/3qIAB1TMj6Gur6hmcDYG7uhIQFyppCzZMgte9+DIZOV7YHGVuvBL0CMRBtDb6+PsOD3oWQ/8Pqzp/dus70AneAXjr0YEkM6ZaRLqQ+xNn55DN3dXrFNm/wf6323u0yAWKcegiG4TNM0BYx5nps0woLZ+o2pgyWwHzI/W1+AzAzFcQysR1EE9vV06q3K127n9VdVBf6yxDd6o2QCNAaGNNs7DNgmV9boevCfN6BfL+9sPD9xpEYAAAAASUVORK5CYII=';
    const darkIcon = '/static/img/oillamp-light-light.gif';

    // Проверка сохраненной темы в localStorage
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add(darkThemeClass);
        themeToggle.src = darkIcon;
    } else {
        themeToggle.src = lightIcon;
    }

    themeToggle.addEventListener('click', function () {
        document.body.classList.toggle(darkThemeClass);

        if (document.body.classList.contains(darkThemeClass)) {
            localStorage.setItem('theme', 'dark');
            themeToggle.src = darkIcon;
        } else {
            localStorage.removeItem('theme');
            themeToggle.src = lightIcon;
        }
    });
});
