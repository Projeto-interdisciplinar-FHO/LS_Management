<!--
  Um único conjunto de ícones de traço, no lugar dos emojis que o app usava.
  Emoji muda de desenho a cada sistema operacional, não herda a cor do texto
  e não tem como ficar alinhado com o resto — por isso a interface parecia
  colada de fontes diferentes.

  Grade de 24×24, traço de 1.6, cantos e pontas arredondados. Os ícones
  genéricos seguem a geometria do Lucide; os do domínio (vaca, estábulo,
  ordenha) foram desenhados na mesma grade para não destoarem.

  Uso: <AppIcon name="animal" /> ou <AppIcon name="trash" :size="14" />
-->
<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    :stroke-width="strokeWidth"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
    focusable="false"
  >
    <path v-for="(d, i) in paths" :key="i" :d="d" />
    <circle
      v-for="(c, i) in circles"
      :key="`c${i}`"
      :cx="c[0]"
      :cy="c[1]"
      :r="c[2]"
    />
  </svg>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  name: { type: String, required: true },
  size: { type: [Number, String], default: 16 },
  strokeWidth: { type: [Number, String], default: 1.6 },
});

// Cada ícone é [ lista de paths, lista de círculos ].
const ICONS = {
  // ---- Navegação e ações ----
  'arrow-left':   [['m12 19-7-7 7-7', 'M19 12H5']],
  'arrow-right':  [['M5 12h14', 'm12 5 7 7-7 7']],
  'chevron-down': [['m6 9 6 6 6-6']],
  'chevron-right':[['m9 18 6-6-6-6']],
  plus:           [['M12 5v14', 'M5 12h14']],
  close:          [['M18 6 6 18', 'm6 6 12 12']],
  check:          [['M20 6 9 17l-5-5']],
  search:         [['m21 21-4.3-4.3'], [[11, 11, 7]]],
  menu:           [['M4 6h16', 'M4 12h16', 'M4 18h16']],
  filter:         [['M3 5h18', 'M7 12h10', 'M10 19h4']],
  edit:           [['M11 4H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5',
                    'M18.4 2.6a2 2 0 0 1 2.8 2.8L12 14.6 8 15.6l1-4Z']],
  trash:          [['M3 6h18', 'M8 6V4.5A1.5 1.5 0 0 1 9.5 3h5A1.5 1.5 0 0 1 16 4.5V6',
                    'M18.5 6 18 19.5a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 6 19.5L5.5 6',
                    'M10 11v5', 'M14 11v5']],
  save:           [['M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2Z',
                    'M17 21v-8H7v8', 'M7 3v5h8']],
  logout:         [['M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4', 'm16 17 5-5-5-5', 'M21 12H9']],
  send:           [['M22 2 11 13', 'm22 2-7 20-4-9-9-4Z']],
  lock:           [['M5 11h14a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2Z',
                    'M7.5 11V7a4.5 4.5 0 0 1 9 0v4']],
  move:           [['m16 3 4 4-4 4', 'M20 7H4', 'm8 21-4-4 4-4', 'M4 17h16']],

  // ---- Domínio: rebanho e manejo ----
  // Vaca de frente: orelhas, cabeça, olhos e focinho.
  animal: [[
    'M6 7C4.3 6.6 3.2 5 3.6 3.6 4 2.2 5.8 2 7.2 3.1',
    'M18 7c1.7-.4 2.8-2 2.4-3.4C20 2.2 18.2 2 16.8 3.1',
    'M7 7h10a1 1 0 0 1 1 1v3.5a5.5 5.5 0 0 1-5.5 5.5h-1A5.5 5.5 0 0 1 6 11.5V8a1 1 0 0 1 1-1Z',
    'M9.5 11h.01', 'M14.5 11h.01',
    'M10 20h4',
  ]],
  // Grupo / lote: camadas empilhadas.
  herd: [[
    'M12.4 2.3a1 1 0 0 0-.8 0L3 6.2a.5.5 0 0 0 0 .9l8.6 3.9a1 1 0 0 0 .8 0L21 7.1a.5.5 0 0 0 0-.9Z',
    'm21 12.6-8.6 3.9a1 1 0 0 1-.8 0L3 12.6',
    'm21 17.1-8.6 3.9a1 1 0 0 1-.8 0L3 17.1',
  ]],
  // Operador de campo: capacete.
  worker: [[
    'M3 18h18a1 1 0 0 0 1-1v-1a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1Z',
    'M10 15V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v10',
    'M5 15v-3a5 5 0 0 1 5-5', 'M14 7a5 5 0 0 1 5 5v3',
  ]],
  barn: [[
    'M3 21V10.2L12 3.8l9 6.4V21', 'M3 21h18',
    'M9.5 21v-5.5h5V21', 'M7.5 11.5h9',
  ]],
  scale: [[
    'M12 4v17', 'M7 21h10', 'M4 7h4l4-1 4 1h4',
    'm4 7-2.5 6a3 3 0 0 0 5 0Z',
    'm20 7-2.5 6a3 3 0 0 0 5 0Z',
  ]],
  milk: [[
    'M9 2h6',
    'M9.5 2v3.3a3 3 0 0 1-.4 1.5l-.7 1.2a3 3 0 0 0-.4 1.5V20a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-10.5a3 3 0 0 0-.4-1.5l-.7-1.2a3 3 0 0 1-.4-1.5V2',
    'M8 15c1.7-.8 3.3-.8 5 0s3.3.8 5 0',
  ]],
  syringe: [[
    'm14 4 6 6', 'm17.5 6.5 3-3', 'm19 9-9.6 9.6a2 2 0 0 1-2.8 0l-2.2-2.2a2 2 0 0 1 0-2.8L14 4',
    'm5 19-2.5 2.5', 'm9.5 10.5 3 3', 'm12.5 7.5 3 3',
  ]],
  stethoscope: [[
    'M5 2v2', 'M11 2v2',
    'M4 3h8v6a4 4 0 0 1-8 0V3Z',
    'M8 13v2a5 5 0 0 0 10 0v-1.2',
  ], [[18, 11, 2.2]]],
  // Trigo: alimento / ração.
  feed: [[
    'M12 22V9',
    'M12 13c-2.2 0-4-1.8-4-4 2.2 0 4 1.8 4 4Z',
    'M12 13c2.2 0 4-1.8 4-4-2.2 0-4 1.8-4 4Z',
    'M12 18c-2.2 0-4-1.8-4-4 2.2 0 4 1.8 4 4Z',
    'M12 18c2.2 0 4-1.8 4-4-2.2 0-4 1.8-4 4Z',
    'M12 8c-1.4-1-1.4-3.5 0-5 1.4 1.5 1.4 4 0 5Z',
  ]],
  dna: [[
    'M7 3c0 5 10 5 10 9s-10 4-10 9',
    'M17 3c0 5-10 5-10 9s10 4 10 9',
    'M8.6 6.5h6.8', 'M8.6 17.5h6.8',
  ]],
  tag: [[
    'M11.6 2.4A2 2 0 0 0 10.2 2H4a2 2 0 0 0-2 2v6.2a2 2 0 0 0 .6 1.4l8.7 8.7a2 2 0 0 0 2.8 0l6.2-6.2a2 2 0 0 0 0-2.8Z',
  ], [[7, 7, 1.3]]],
  chart:     [['M3 3v16a2 2 0 0 0 2 2h16', 'm7 14 3.5-4.5L14 13l4.5-6']],
  report:    [['M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z',
               'M14 2v6h6', 'M9 13h6', 'M9 17h4']],
  clipboard: [['M9 4H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-3',
               'M9.5 2h5a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-5a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1Z',
               'M12 12h4', 'M12 16h4', 'M8.5 12h.01', 'M8.5 16h.01']],
  users:     [['M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2',
               'M22 21v-2a4 4 0 0 0-3-3.9', 'M16 3.1a4 4 0 0 1 0 7.8'], [[9, 7, 4]]],
  calendar:  [['M5 4h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Z',
               'M16 2v4', 'M8 2v4', 'M3 10h18']],
  clock:     [['M12 7.5V12l3 1.8'], [[12, 12, 9]]],

  // ---- Estado e feedback ----
  alert:          [['M12 9v4.5', 'M12 17.5h.01',
                    'M10.3 3.9 1.9 18a2 2 0 0 0 1.7 3h16.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z']],
  info:           [['M12 16.5V11.5', 'M12 8h.01'], [[12, 12, 9]]],
  'check-circle': [['m8.2 12.3 2.5 2.5 5.1-5.1'], [[12, 12, 9]]],
  'x-circle':     [['m15 9-6 6', 'm9 9 6 6'], [[12, 12, 9]]],
  inbox:          [['M22 12h-5.5l-1.5 2.5h-6L7.5 12H2',
                    'M5.4 5.1 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.4-6.9A2 2 0 0 0 16.8 4H7.2a2 2 0 0 0-1.8 1.1Z']],
  bell:           [['M18 8.5a6 6 0 1 0-12 0c0 6.5-2.5 8.5-2.5 8.5h17S18 15 18 8.5',
                    'M13.7 20.5a2 2 0 0 1-3.4 0']],
  sun:            [['M12 2.5v2M12 19.5v2M4.6 4.6l1.4 1.4M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4'],
                   [[12, 12, 4]]],
  moon:           [['M20.8 13.4A8.5 8.5 0 1 1 10.6 3.2a6.6 6.6 0 0 0 10.2 10.2Z']],
  sparkle:        [['M12 3l1.6 5.4L19 10l-5.4 1.6L12 17l-1.6-5.4L5 10l5.4-1.6Z',
                    'M18.5 15.5 19 17.5l2 .5-2 .5-.5 2-.5-2-2-.5 2-.5Z']],
};

const entry = computed(() => ICONS[props.name] || ICONS.info);
const paths = computed(() => entry.value[0] || []);
const circles = computed(() => entry.value[1] || []);
</script>
