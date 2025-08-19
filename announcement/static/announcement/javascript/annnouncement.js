function toggleContent(element) {
        const fullContent = element.querySelector('.full-content');
        const shortContent = element.querySelector('.short-content');
        if (shortContent.style.display === 'none') {
            shortContent.style.display = 'block';
            fullContent.style.display = 'none';

        } else {
            shortContent.style.display = 'none';
            fullContent.style.display = 'block';

        }
    }