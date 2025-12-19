let currentDate = new Date();
let completedDays = new Set();
let currentView = 'month';

document.addEventListener('DOMContentLoaded', async () => {
    await loadData();
    renderMonth();
    setupListeners();
});

async function loadData() {
    try {
        const res = await fetch('/api/days');
        const data = await res.json();
        completedDays = new Set(data.completed_days);
        updateStats();
    } catch (err) {
        console.error('Error loading data:', err);
    }
}

function setupListeners() {
    document.getElementById('prevMonth').onclick = () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderMonthWithAnimation('prev');
    };

    document.getElementById('nextMonth').onclick = () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderMonthWithAnimation('next');
    };

    document.getElementById('todayBtn').onclick = () => {
        currentDate = new Date();
        if (currentView === 'year') switchView();
        renderMonth();
    };

    document.getElementById('yearViewBtn').onclick = switchView;

    document.getElementById('prevYear').onclick = () => {
        currentDate.setFullYear(currentDate.getFullYear() - 1);
        renderYearWithAnimation('prev');
    };

    document.getElementById('nextYear').onclick = () => {
        currentDate.setFullYear(currentDate.getFullYear() + 1);
        renderYearWithAnimation('next');
    };

    document.getElementById('exportJson').onclick = (e) => {
        e.preventDefault();
        window.location.href = '/api/export/json';
    };

    document.getElementById('exportCsv').onclick = (e) => {
        e.preventDefault();
        window.location.href = '/api/export/csv';
    };
}

function switchView() {
    currentView = currentView === 'month' ? 'year' : 'month';
    const monthView = document.getElementById('monthView');
    const yearView = document.getElementById('yearView');
    const monthNavControls = document.getElementById('monthNavControls');
    const btn = document.getElementById('yearViewBtn');

    if (currentView === 'year') {
        monthView.className = 'view-hidden';
        yearView.className = 'view-active';
        monthNavControls.style.display = 'none';
        btn.textContent = 'Month View';
        renderYear();
    } else {
        monthView.className = 'view-active';
        yearView.className = 'view-hidden';
        monthNavControls.style.display = 'flex';
        btn.textContent = 'Year View';
        renderMonth();
    }
}

function renderMonthWithAnimation(direction) {
    const grid = document.getElementById('calendarDays');
    grid.classList.add('transitioning');
    
    if (direction === 'prev') {
        grid.classList.add('slide-left');
    } else if (direction === 'next') {
        grid.classList.add('slide-right');
    }
    
    setTimeout(() => {
        renderMonth();
        grid.classList.remove('transitioning', 'slide-left', 'slide-right');
    }, 300);
}

function renderMonth() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const months = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'];

    document.getElementById('currentMonth').textContent = `${months[month]} ${year}`;

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const prevMonthDays = new Date(year, month, 0).getDate();

    const grid = document.getElementById('calendarDays');
    grid.innerHTML = '';

    const today = new Date();
    const isThisMonth = today.getFullYear() === year && today.getMonth() === month;

    // Previous month days
    for (let i = firstDay - 1; i >= 0; i--) {
        const day = prevMonthDays - i;
        const el = makeDay(day, true);
        grid.appendChild(el);
    }

    // Current month days
    for (let day = 1; day <= daysInMonth; day++) {
        const dateStr = `${year}-${pad(month + 1)}-${pad(day)}`;
        const el = makeDay(day, false);

        if (isThisMonth && day === today.getDate()) {
            el.classList.add('today');
        }

        if (completedDays.has(dateStr)) {
            el.classList.add('completed');
        }

        el.onclick = () => toggleDay(dateStr, el);
        grid.appendChild(el);
    }

    // Next month days
    const totalCells = grid.children.length;
    const remaining = 42 - totalCells;
    for (let day = 1; day <= remaining; day++) {
        const el = makeDay(day, true);
        grid.appendChild(el);
    }

    updateStats();
}

function renderYearWithAnimation(direction) {
    const grid = document.getElementById('yearGrid');
    grid.classList.add('transitioning');
    
    if (direction === 'prev') {
        grid.classList.add('slide-left');
    } else if (direction === 'next') {
        grid.classList.add('slide-right');
    }
    
    setTimeout(() => {
        renderYear();
        grid.classList.remove('transitioning', 'slide-left', 'slide-right');
    }, 300);
}

function renderYear() {
    const year = currentDate.getFullYear();
    document.getElementById('currentYear').textContent = year;
    const grid = document.getElementById('yearGrid');
    grid.innerHTML = '';

    const months = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'];

    for (let m = 0; m < 12; m++) {
        const container = document.createElement('div');
        container.className = 'mini-month';

        const title = document.createElement('h3');
        title.textContent = months[m];
        container.appendChild(title);

        const weekdays = document.createElement('div');
        weekdays.className = 'weekdays';
        ['S', 'M', 'T', 'W', 'T', 'F', 'S'].forEach(d => {
            const span = document.createElement('div');
            span.textContent = d;
            weekdays.appendChild(span);
        });
        container.appendChild(weekdays);

        const daysGrid = document.createElement('div');
        daysGrid.className = 'days-grid';

        const firstDay = new Date(year, m, 1).getDay();
        const daysInMonth = new Date(year, m + 1, 0).getDate();

        for (let i = 0; i < firstDay; i++) {
            const empty = document.createElement('div');
            empty.className = 'day other-month';
            daysGrid.appendChild(empty);
        }

        for (let d = 1; d <= daysInMonth; d++) {
            const dateStr = `${year}-${pad(m + 1)}-${pad(d)}`;
            const el = makeDay(d, false);

            if (completedDays.has(dateStr)) {
                el.classList.add('completed');
            }

            el.onclick = async () => {
                await toggleDay(dateStr, el);
            };

            daysGrid.appendChild(el);
        }

        container.appendChild(daysGrid);
        grid.appendChild(container);
    }
}

function makeDay(num, isOther) {
    const el = document.createElement('div');
    el.className = 'day';
    el.textContent = num;
    if (isOther) el.classList.add('other-month');
    return el;
}

async function toggleDay(dateStr, el) {
    try {
        const res = await fetch(`/api/days/${dateStr}`, { method: 'POST' });
        const data = await res.json();

        if (data.success) {
            if (data.completed) {
                completedDays.add(dateStr);
                el.classList.add('completed');
            } else {
                completedDays.delete(dateStr);
                el.classList.remove('completed');
            }
            updateStats();
        }
    } catch (err) {
        console.error('Error toggling day:', err);
    }
}

function updateStats() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    let monthCount = 0;
    completedDays.forEach(dateStr => {
        const d = new Date(dateStr);
        if (d.getFullYear() === year && d.getMonth() === month) {
            monthCount++;
        }
    });

    document.getElementById('monthCount').textContent = monthCount;
    document.getElementById('totalCount').textContent = completedDays.size;
}

function pad(n) {
    return String(n).padStart(2, '0');
}
