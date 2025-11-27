// Основные JavaScript функции для сайта
document.addEventListener('DOMContentLoaded', function() {
    // Анимация появления элементов
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.custom-card, .stat-card');
        
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.style.opacity = "1";
                element.style.transform = "translateY(0)";
            }
        });
    };

    // Установка начальных стилей для анимации
    const cards = document.querySelectorAll('.custom-card, .stat-card');
    cards.forEach(card => {
        card.style.opacity = "0";
        card.style.transform = "translateY(20px)";
        card.style.transition = "opacity 0.6s ease, transform 0.6s ease";
    });

    // Запуск анимации при загрузке и скролле
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll();

    // Подтверждение действий
    const confirmActions = function() {
        const deleteButtons = document.querySelectorAll('.btn-outline-danger');
        
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                if (!confirm('Вы уверены, что хотите выполнить это действие?')) {
                    e.preventDefault();
                }
            });
        });
    };

    confirmActions();

    // Динамическое обновление времени
    const updateTime = function() {
        const timeElements = document.querySelectorAll('.update-time');
        const now = new Date();
        
        timeElements.forEach(element => {
            element.textContent = now.toLocaleTimeString('ru-RU');
        });
    };

    setInterval(updateTime, 60000);

    // Плавная прокрутка для якорей
    const smoothScroll = function() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    };

    smoothScroll();

    // Уведомления
    const showNotification = function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show`;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Добавляем кастомные стили для уведомлений
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '9999';
        notification.style.minWidth = '300px';
        
        document.body.appendChild(notification);
        
        // Автоматическое скрытие через 5 секунд
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    };

    // Глобальная функция для показа уведомлений
    window.showNotification = showNotification;

    // Обработка форм с подтверждением
    const handleFormSubmissions = function() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                const submitBtn = this.querySelector('button[type="submit"]');
                
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Обработка...';
                    
                    // Автоматическое восстановление кнопки через 10 секунд на случай ошибки
                    setTimeout(() => {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = submitBtn.getAttribute('data-original-text') || 'Отправить';
                    }, 10000);
                }
            });
        });
    };

    handleFormSubmissions();

    console.log('🎮 Game Club System initialized successfully!');
});

// Дополнительные функции для админ-панели
function adminFunctions() {
    // Быстрое переключение статусов
    const quickToggle = document.querySelectorAll('.quick-toggle');
    quickToggle.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const form = this.closest('form');
            if (form) {
                form.submit();
            }
        });
    });

    // Поиск в таблицах
    const initTableSearch = function() {
        const searchInputs = document.querySelectorAll('.table-search');
        
        searchInputs.forEach(input => {
            input.addEventListener('input', function() {
                const filter = this.value.toLowerCase();
                const table = this.closest('.card').querySelector('table');
                const rows = table.querySelectorAll('tbody tr');
                
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(filter) ? '' : 'none';
                });
            });
        });
    };

    initTableSearch();
}

// Инициализация админских функций при загрузке
if (document.querySelector('.admin-dashboard')) {
    document.addEventListener('DOMContentLoaded', adminFunctions);
}