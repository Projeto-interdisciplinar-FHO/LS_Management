<template>
  <div class="page-wrapper">
    <header class="page-header">
      <button @click="$router.back()" class="btn-back">← Voltar</button>
      <div class="header-content">
        <h1>Relatórios de Gestão</h1>
        <p>Análise e evolução dos dados do rebanho.</p>
      </div>
    </header>

    <div class="content-container">
      <div class="tabs-container">
        <button class="tab active">📈 Evolução de Peso</button>
        <button class="tab">🥛 Produção de Leite</button>
        <button class="tab">✛ Imunização</button>
      </div>

      <section class="report-card">
        <header class="card-header">
          <h2>Resumo Geral do Rebanho</h2>
          <button class="btn-outline">Exportar PDF</button>
        </header>

        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>Animal (Brinco)</th>
                <th>Peso Inicial</th>
                <th>Peso Atual</th>
                <th>Variação</th>
                <th>Status de Ganho</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="font-bold">#142</td>
                <td>420 kg</td>
                <td>450 kg</td>
                <td class="text-green">+30 kg</td>
                <td><span class="badge badge-good">Excelente</span></td>
              </tr>
              <tr>
                <td class="font-bold">#089</td>
                <td>310 kg</td>
                <td>305 kg</td>
                <td class="text-red">-5 kg</td>
                <td><span class="badge badge-bad">Alerta</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
// Lógica de relatórios será integrada com a API aqui
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
.page-wrapper { padding: 40px; background-color: #f8fafc; min-height: 100vh; font-family: 'Inter', sans-serif; color: #0f172a; }
.page-header { margin-bottom: 32px; }
.btn-back { background: transparent; border: 1px solid #e2e8f0; color: #64748b; padding: 8px 16px; border-radius: 8px; cursor: pointer; margin-bottom: 16px; font-weight: 500; }
.btn-back:hover { background: #f1f5f9; color: #0f172a; }
.header-content h1 { font-size: 2rem; font-weight: 700; margin-bottom: 8px; }
.header-content p { color: #64748b; }

.content-container { max-width: 1000px; }

.tabs-container { display: flex; gap: 8px; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; overflow-x: auto; }
.tab { background: transparent; border: none; padding: 10px 20px; font-size: 0.95rem; font-weight: 600; color: #64748b; cursor: pointer; border-radius: 8px; transition: 0.2s; white-space: nowrap; }
.tab:hover { background: #f1f5f9; color: #0f172a; }
.tab.active { background: #f0fdf4; color: #16a34a; }

.report-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.card-header h2 { font-size: 1.25rem; font-weight: 600; margin: 0; }
.btn-outline { background: transparent; border: 1px solid #cbd5e1; color: #0f172a; padding: 8px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; }
.btn-outline:hover { background: #f1f5f9; }

.table-responsive { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; text-align: left; }
.data-table th { background: #f8fafc; padding: 16px; font-size: 0.85rem; text-transform: uppercase; color: #64748b; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
.data-table td { padding: 16px; border-bottom: 1px solid #e2e8f0; font-size: 0.95rem; color: #0f172a; }
.data-table tr:hover { background: #f8fafc; }
.data-table tr:last-child td { border-bottom: none; }

.font-bold { font-weight: 600; font-family: monospace; font-size: 1.05rem; }
.text-green { color: #16a34a; font-weight: 600; }
.text-red { color: #ef4444; font-weight: 600; }

.badge { padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
.badge-good { background: #dcfce7; color: #166534; }
.badge-bad { background: #fef2f2; color: #991b1b; }
</style>