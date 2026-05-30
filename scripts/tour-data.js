/* ============================================================
   VIBE TURISTIC — shared tour data + render helpers
   Exposes window.VIBE. Sprite base configurable via window.VIBE_SPRITE.
   ============================================================ */
window.VIBE = (function () {
  'use strict';
  var SP = (typeof window.VIBE_SPRITE === 'string') ? window.VIBE_SPRITE : '';
  function ic(id, style) {
    return '<svg class="i"' + (style ? ' style="' + style + '"' : '') + '><use href="' + SP + '#' + id + '"></use></svg>';
  }

  var TOURS = {
    '3': {
      key: '3', title: 'Зимний тур', dur: '3 дня / 2 ночи', durShort: '3 дня',
      price: '33 000', prepay: '10 000', group: 'до 18', meet: '8:30', back: 'после 20:00',
      badge: 'Уикенд', href: 'tours/tour-3.html',
      hero: 'https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=1600&q=80',
      card: 'https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=900&q=80',
      tagline: 'Насыщенный уикенд для тех, у кого мало времени, но много энергии.',
      cardName: 'Тур 3 дня', cardSub: 'Насыщенный уикенд',
      cardTag: 'Для тех, у кого мало времени, но много энергии. Всё самое яркое за выходные.',
      durIcon: 'i-mountain', feats: ['до 18 человек', 'всё включено', 'актив'],
      priceLabel: 'за человека', cardCta: 'Подробнее о туре', cardCtaStyle: 'btn--blue',
      meta: ['❄️ Насыщенный уикенд', '📍 старт — Махачкала', '🏔️ 3 дня / 2 ночи в горах'],
      included: [
        ['i-bus', 'Транспорт на все <b>3 дня</b> между всеми достопримечательностями'],
        ['i-mountain', 'Проживание в горах <b>3 дня / 2 ночи</b> в гостевом доме'],
        ['i-coffee', 'Питание — полноценные завтраки, обеды и ужины'],
        ['i-guide', 'Работа сертифицированного гида'],
        ['i-swim', 'Прогулка на SUP-досках по водохранилищу'],
        ['i-boat', 'Прогулка на катере'],
        ['i-star', 'Все экскурсии и входные билеты'],
        ['i-coffee', 'Кофе-тайм на природе']
      ]
    },
    '5': {
      key: '5', title: 'Зимний тур', dur: '5 дней / 4 ночи', durShort: '5 дней',
      price: '42 000', prepay: '15 000', group: 'до 18', meet: '8:30', back: 'после 20:00',
      badge: 'Хит сезона', href: 'tours/tour-5.html',
      hero: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1600&q=80',
      card: 'https://images.unsplash.com/photo-1500964757637-c85e8a162699?w=900&q=80',
      tagline: 'Полное погружение в Дагестан: горы, вода, барханы и новые друзья.',
      cardName: 'Тур 5 дней', cardSub: 'Полное погружение',
      cardTag: 'Горы, вода, барханы и новые друзья — максимум Дагестана за пять дней.',
      durIcon: 'i-mountain', feats: ['до 18 человек', 'всё включено', 'SUP + катер'],
      priceLabel: 'за человека', cardCta: 'Подробнее о туре', cardCtaStyle: 'btn--blue',
      meta: ['❄️ Полное погружение', '📍 старт — Махачкала', '🏔️ 5 дней / 4 ночи в горах'],
      included: [
        ['i-bus', 'Транспорт на все <b>5 дней</b> между всеми достопримечательностями'],
        ['i-mountain', 'Проживание в горах <b>5 дней / 4 ночи</b> в гостевом доме'],
        ['i-coffee', 'Питание — полноценные завтраки, обеды и ужины'],
        ['i-guide', 'Работа сертифицированного гида'],
        ['i-swim', 'Прогулка на SUP-досках по водохранилищу'],
        ['i-boat', 'Прогулка на катере'],
        ['i-star', 'Все экскурсии и входные билеты'],
        ['i-coffee', 'Кофе-тайм на природе']
      ]
    },
    'custom': {
      key: 'custom', custom: true, href: '#ask',
      badge: 'Под тебя', durIcon: 'i-heart', dur: 'свои даты и маршрут',
      card: 'https://images.unsplash.com/photo-1539635278303-d4002c07eae3?w=900&q=80',
      cardName: 'Индивидуальный тур', cardSub: 'Только ваша компания',
      cardTag: 'Свои даты, свой маршрут и состав группы. Соберём тур мечты под ваш запрос.',
      feats: ['свои даты', 'свой маршрут', 'любой состав'],
      price: 'Цена по запросу', priceLabel: '', cardCta: 'Рассчитать цену', cardCtaStyle: 'btn--neon'
    }
  };

  // Order of cards shown on the home page
  var TOUR_ORDER = ['5', '3', 'custom'];

  var NOT_INCLUDED = [
    'Авиа- или ж/д-билеты из вашего города до Махачкалы и обратно',
    'Личные траты на сувениры',
    'Спиртное',
    'Кофе и чай в кафе на остановках',
    'Экстремальные виды развлечений',
    'Всё остальное, что не указано выше'
  ];

  var TAKE = [
    ['i-swim', 'Купальник / шорты', 'для воды и SUP'],
    ['i-hat', 'Головной убор', 'кепка или панама'],
    ['i-glasses', 'Солнцезащитные очки', 'в горах ярко'],
    ['i-sun', 'Солнцезащитный крем', 'SPF 30+'],
    ['i-shoe', 'Удобная обувь', 'можно тапочки'],
    ['i-umbrella', 'Дождевик', 'на случай пасмурной погоды'],
    ['i-cash', 'Наличные деньги', 'карманные расходы'],
    ['i-jacket', 'Тёплая одежда', 'вечером в горах прохладно'],
    ['i-battery', 'Зарядка / powerbank', 'для всех гаджетов']
  ];

  // Schedule rows: [dates, tourType, seatsClass, label]
  var SCHED = [
    { mo: 'Декабрь', yr: '2025', cls: 'm-dec', rows: [
      ['12–14', '3', 'low', '3 места'], ['19–23', '5', 'ok', 'есть места'], ['26–30', '5', 'ok', 'есть места'] ] },
    { mo: 'Январь', yr: '2026', cls: 'm-jan', rows: [
      ['02–06', '5', 'full', 'нет мест'], ['09–11', '3', 'ok', 'есть места'], ['16–20', '5', 'low', '5 мест'], ['23–27', '5', 'ok', 'есть места'] ] },
    { mo: 'Февраль', yr: '2026', cls: 'm-feb', rows: [
      ['06–08', '3', 'ok', 'есть места'], ['13–17', '5', 'ok', 'есть места'], ['20–24', '5', 'low', '4 места'] ] }
  ];

  // Gallery photos for tour pages: [src, caption, sizeClass]
  var GALLERY = [
    ['https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=900&q=80', 'Горный массив', 'tall'],
    ['https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=900&q=80', 'Сулакский каньон', ''],
    ['https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=900&q=80', 'Водопады', ''],
    ['https://images.unsplash.com/photo-1530053969600-caed2596d242?w=900&q=80', 'SUP по воде', 'wide'],
    ['https://images.unsplash.com/photo-1473580044384-7ba9967e16a0?w=900&q=80', 'Бархан Сарыкум', ''],
    ['https://images.unsplash.com/photo-1500964757637-c85e8a162699?w=900&q=80', 'Гостевой дом', ''],
    ['https://images.unsplash.com/photo-1539635278303-d4002c07eae3?w=900&q=80', 'Наша группа', 'wide'],
    ['https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=900&q=80', 'Виды Кавказа', '']
  ];

  function renderGallery(el) {
    if (!el) return;
    el.innerHTML = GALLERY.map(function (g) {
      return '<figure class="photostrip__cell">' +
        '<img src="' + g[0] + '" alt="' + g[1] + '" loading="lazy"></figure>';
    }).join('');
  }

  var REVIEWS = [
    ['Алина', 'Москва', 'AЛ', '#28B5FF', '5-дневный тур', 'Лучшие 5 дней за год! Гид топовый, локации космос, а группа стала семьёй уже на второй день. SUP на рассвете — отдельная любовь.'],
    ['Тимур', 'Казань', 'ТМ', '#FF6FA5', '3-дневный тур', 'Брал короткий формат на выходные — успели нереально много. Всё чётко по организации, ни одной заминки.'],
    ['Дарья', 'СПб', 'ДР', '#19D3A2', '5-дневный тур', 'Каньон, водопады, бархан — каждый день новая картинка. Рилсы залетели на сотни тысяч просмотров 😍'],
    ['Игорь', 'Екатеринбург', 'ИГ', '#7C5BFF', '5-дневный тур', 'Думал будет туристический конвейер — оказалось живое приключение. Питание домашнее, порции огромные.'],
    ['Камилла', 'Уфа', 'КМ', '#F4A100', '3-дневный тур', 'Первый раз в Дагестане и сразу влюбилась. Ребята помогли с отелем до тура, всё на высшем уровне.'],
    ['Никита', 'Новосибирск', 'НК', '#0E9C7E', '5-дневный тур', 'Маленькая группа — это кайф. Никакой толпы, успеваешь поговорить с гидом и реально проникнуться местом.'],
    ['Вероника', 'Краснодар', 'ВР', '#E0246B', '5-дневный тур', 'Барханы Сарыкум на закате — вау. Организация 10 из 10, вернусь летом точно.'],
    ['Артём', 'Самара', 'АР', '#0B6FD0', '3-дневный тур', 'Катер, горы, кофе-тайм на скале с видом на каньон. За три дня впечатлений как за отпуск.']
  ];

  function renderInfoGrid(el, key) {
    if (!el) return;
    var t = TOURS[key];
    var cards = [
      { cls: 'c-price span6', q: 'Сколько стоит тур?', qic: 'i-wallet', v: t.price + ' <small>₽</small>', sub: 'за человека' },
      { cls: 'c-pre', q: 'Сколько предоплата?', qic: 'i-card', v: t.prepay + ' <small>₽</small>', sub: 'для брони места' },
      { cls: 'c-grp', q: 'Сколько человек в группе?', qic: 'i-people', v: t.group + ' <small>чел.</small>', sub: 'маленькая компания' },
      { cls: 'c-meet', q: 'Во сколько сбор тура?', qic: 'i-sunrise', v: t.meet + ' <small>утра</small>', sub: 'в день старта' },
      { cls: 'c-back', q: 'Во сколько вылет обратно?', qic: 'i-plane', v: t.back, sub: 'в день отъезда' }
    ];
    el.innerHTML = cards.map(function (c) {
      return '<article class="infocard ' + c.cls + '">' +
        '<div class="q"><span class="qic">' + ic(c.qic) + '</span>' + c.q + '</div>' +
        '<div><div class="v">' + c.v + '</div><div class="sub">' + c.sub + '</div></div></article>';
    }).join('');
  }
  function renderIncluded(el, key) {
    if (!el) return;
    el.innerHTML = TOURS[key].included.map(function (row) {
      return '<li><span class="mk">' + ic('i-check') + '</span><span>' + row[1] + '</span></li>';
    }).join('');
  }
  function renderNotIncluded(el) {
    if (!el) return;
    el.innerHTML = NOT_INCLUDED.map(function (txt) {
      return '<li><span class="mk">' + ic('i-x') + '</span><span>' + txt + '</span></li>';
    }).join('');
  }
  function renderTake(el) {
    if (!el) return;
    el.innerHTML = TAKE.map(function (r) {
      return '<div class="takecard"><span class="tic">' + ic(r[0]) + '</span><b>' + r[1] + '</b><span>' + r[2] + '</span></div>';
    }).join('') +
      '<div class="takecard fun"><span class="tic">' + ic('i-smile') + '</span><b>Хорошее настроение</b><span>самое важное 🐑</span></div>';
  }
  function renderScheduleCards(el) {
    if (!el) return;
    el.innerHTML = SCHED.map(function (m) {
      return '<div class="schedcard"><div class="schedcard__top ' + m.cls + '">' +
        '<div><div class="mo">' + m.mo + '</div><div class="yr">' + m.yr + '</div></div>' +
        ic('i-calendar', 'width:26px;height:26px') + '</div><div class="schedcard__body">' +
        m.rows.map(function (r) {
          return '<div class="schedrow"><div class="dt">' + r[0] + '<small>тур на ' + (r[1] === '3' ? '3 дня' : '5 дней') + '</small></div>' +
            '<span class="seats ' + r[2] + '">' + r[3] + '</span></div>';
        }).join('') + '</div></div>';
    }).join('');
  }
  function renderTourDates(el, key) {
    if (!el) return;
    var rows = [];
    SCHED.forEach(function (m) {
      m.rows.forEach(function (r) {
        if (r[1] === key) rows.push([m.mo + ' ' + m.yr, r[0], r[2], r[3]]);
      });
    });
    el.innerHTML = rows.map(function (r) {
      return '<div class="datechip"><div class="datechip__d">' + r[1] + '<small>' + r[0] + '</small></div>' +
        '<span class="seats ' + r[2] + '">' + r[3] + '</span></div>';
    }).join('');
  }
  function renderTourCards(el) {
    if (!el) return;
    el.innerHTML = TOUR_ORDER.map(function (k) {
      var t = TOURS[k];
      var priceHtml = t.priceLabel
        ? '<b>' + t.price + ' ₽</b><small>' + t.priceLabel + '</small>'
        : '<b>' + t.price + '</b>';
      return '<a class="tcard' + (t.custom ? ' indiv' : '') + '" href="' + t.href + '">' +
        '<div class="tcard__media">' +
          '<img src="' + t.card + '" alt="' + t.cardName + '">' +
          '<span class="tcard__badge">' + t.badge + '</span>' +
          '<span class="tcard__dur">' + ic(t.durIcon, 'width:18px') + ' ' + t.dur + '</span>' +
        '</div>' +
        '<div class="tcard__body">' +
          '<h3 class="tcard__title">' + t.cardName + '<span>' + t.cardSub + '</span></h3>' +
          '<p class="tcard__tag">' + t.cardTag + '</p>' +
          '<ul class="tcard__feats">' + t.feats.map(function (f) { return '<li>' + f + '</li>'; }).join('') + '</ul>' +
          '<div class="tcard__price">' + priceHtml + '</div>' +
          '<div class="tcard__cta"><span class="btn ' + t.cardCtaStyle + '">' + t.cardCta +
            ' ' + ic('i-arrow', 'width:18px;height:18px') + '</span></div>' +
        '</div></a>';
    }).join('');
  }

  function renderReviews(el) {
    if (!el) return;
    el.innerHTML = REVIEWS.map(function (r) {
      return '<div class="revcard"><div class="revcard__top">' +
        '<span class="revcard__av" style="background:' + r[3] + '">' + r[2] + '</span>' +
        '<span class="revcard__nm">' + r[0] + '<small>' + r[1] + '</small></span>' +
        '<span class="revcard__stars">★★★★★</span></div><p>' + r[4] + '</p>' +
        '<div class="tour-tag">' + r[5] + '</div></div>';
    }).join('');
  }

  return {
    TOURS: TOURS, NOT_INCLUDED: NOT_INCLUDED, SCHED: SCHED, REVIEWS: REVIEWS, ic: ic,
    renderInfoGrid: renderInfoGrid, renderIncluded: renderIncluded, renderNotIncluded: renderNotIncluded,
    renderTake: renderTake, renderScheduleCards: renderScheduleCards, renderTourDates: renderTourDates,
    renderReviews: renderReviews, renderGallery: renderGallery, renderTourCards: renderTourCards
  };
})();
