/* ============================================================
   VIBE TURISTIC — Tweaks
   ============================================================ */
const { useState, useEffect } = React;

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "palette": "Небо",
  "cards": "Заливка",
  "radius": 34,
  "sheep": true,
  "slogan": "🤘 №1 молодёжные туры по Дагестану"
}/*EDITMODE-END*/;

const PALETTE = { 'Небо': 'sky', 'Бирюза': 'teal', 'Закат': 'sunset' };
const CARDS = { 'Заливка': 'solid', 'Стекло': 'glass', 'Контур': 'outline' };

function VibeTweaks() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);

  useEffect(() => {
    const b = document.body, r = document.documentElement.style;
    b.dataset.palette = PALETTE[t.palette] || 'sky';
    b.dataset.cards = CARDS[t.cards] || 'solid';
    b.dataset.sheep = t.sheep ? 'on' : 'off';
    r.setProperty('--r-lg', t.radius + 'px');
    r.setProperty('--r-md', Math.round(t.radius * 0.65) + 'px');
    r.setProperty('--r-xl', Math.round(t.radius * 1.35) + 'px');
    const rib = document.querySelector('.ribbon');
    if (rib) rib.textContent = t.slogan;
  }, [t.palette, t.cards, t.radius, t.sheep, t.slogan]);

  return (
    <TweaksPanel title="Tweaks">
      <TweakSection label="Палитра" />
      <TweakRadio label="Тема" value={t.palette}
        options={['Небо', 'Бирюза', 'Закат']}
        onChange={(v) => setTweak('palette', v)} />

      <TweakSection label="Карточки тура" />
      <TweakRadio label="Стиль" value={t.cards}
        options={['Заливка', 'Стекло', 'Контур']}
        onChange={(v) => setTweak('cards', v)} />
      <TweakSlider label="Скругление" value={t.radius} min={6} max={46} unit="px"
        onChange={(v) => setTweak('radius', v)} />

      <TweakSection label="Фишки" />
      <TweakToggle label="Барашки-пасхалки 🐑" value={t.sheep}
        onChange={(v) => setTweak('sheep', v)} />
      <TweakText label="Слоган в шапке" value={t.slogan}
        onChange={(v) => setTweak('slogan', v)} />
    </TweaksPanel>
  );
}

ReactDOM.createRoot(document.getElementById('tweaks-root')).render(<VibeTweaks />);
