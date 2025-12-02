document.addEventListener('DOMContentLoaded', function() {
    console.log('Página carregada e scripts prontos!');

    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in-out';
        document.body.style.opacity = '1';
    }, 100);

    const listaTarefasDiv = document.getElementById('listaTarefas');
    const formTarefa = document.getElementById('formTarefa');

    const LIST_URL = '/api/tarefas'; 
    const ADD_URL = '/api/tarefas/add'; 
    
    // ---------------------------------------------
    // FUNÇÕES DE UTILIDADE
    // ---------------------------------------------

    function formatarData(dtString) {
        if (!dtString) return '';
        try {
            const dt = new Date(dtString.replace('T', ' '));
            
            if (!isNaN(dt.getTime())) {
                const isDateTime = dtString.includes('T') && dtString.includes(':');

                if (isDateTime) {
                    return dt.toLocaleDateString('pt-BR') + ' ' + dt.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
                } else {
                    return dt.toLocaleDateString('pt-BR');
                }
            }
        } catch (e) {
            return dtString;
        }
        return dtString;
    }

    // ---------------------------------------------
    // LÓGICA DE TOGGLE DE STATUS (Implementação da interatividade)
    // ---------------------------------------------
    
    async function toggleTarefaStatus(tarefaId, newStatus) {
        const TOGGLE_URL = `/api/tarefas/toggle/${tarefaId}`;
        try {
            const response = await fetch(TOGGLE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                // Envia o novo status como JSON
                body: JSON.stringify({ isConcluida: newStatus }) 
            });

            if (response.ok) {
                console.log(`Tarefa ${tarefaId} atualizada para ${newStatus}`);
                // Recarrega a lista para atualizar o visual
                carregarTarefas(); 
            } else {
                alert('Falha ao alternar status. Verifique o console.');
                console.error('Falha ao alternar status:', response.status);
            }

        } catch (error) {
            console.error('Erro de conexão ao alternar status:', error);
        }
    }

    function adicionarListenersToggle() {
        document.querySelectorAll('.toggle-concluida').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const id = parseInt(e.target.dataset.id);
                const newStatus = e.target.checked;
                toggleTarefaStatus(id, newStatus);
            });
        });
    }

    // ---------------------------------------------
    // CARREGAMENTO E RENDERIZAÇÃO DA LISTA
    // ---------------------------------------------

    async function carregarTarefas() {
        listaTarefasDiv.innerHTML = '<p style="text-align: center;">Carregando tarefas...</p>';
        try {
            const response = await fetch(LIST_URL); 
            
            if (!response.ok) {
                throw new Error(`Erro HTTP! Status: ${response.status}. Verifique o terminal do Bottle.`);
            }
            const data = await response.json();
            const tarefas = data.tarefas || []; 

            listaTarefasDiv.innerHTML = ''; 
            
            if (tarefas.length === 0) {
                listaTarefasDiv.innerHTML = '<p style="text-align: center;">Nenhuma tarefa cadastrada.</p>';
                return;
            }

            const ul = document.createElement('ul');
            tarefas.forEach(t => {
                const li = document.createElement('li');
                
                // 🟢 NOVO: Checkbox (Toggle Status)
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.checked = t.isConcluida;
                checkbox.classList.add('toggle-concluida');
                checkbox.dataset.id = t.id; // ID para o listener
                
                // Estrutura de dados (sem status na frente do nome, pois temos o checkbox)
                const prioridadeTag = `<strong class="tag-${t.prioridade.toLowerCase()}">${t.prioridade.toUpperCase()}</strong>`;
        
                const vencimento = t.data_vencimento ? `Prazo: ${formatarData(t.data_vencimento)}` : '';
                const inicio = formatarData(t.data_hora_inicio);
                const fim = formatarData(t.data_hora_fim);
                const duracao = t.duration_hours ? ` (${t.duration_hours}h)` : '';

                let detalhesData = '';
                if (inicio && fim) {
                    detalhesData += `<span>⏰ Agendado: ${inicio} a ${fim} ${duracao}</span>`;
                } else if (vencimento) {
                    detalhesData += `<span>🗓️ ${vencimento}</span>`;
                }

                if (t.isConcluida) {
                    li.classList.add('concluida');
                }
                
                // 🟢 NOVO: Estrutura HTML ajustada para o CSS (div.tarefa-content)
                li.innerHTML = `
                    <div class="tarefa-content">
                        <div class="tarefa-header">
                            ${prioridadeTag} <span style="font-weight: bold;">${t.nome}</span>
                        </div>
                        <span class="descricao-text">${t.descricao}</span>
                        ${detalhesData}
                    </div>
                `;
                
                // Insere o checkbox antes do conteúdo
                li.prepend(checkbox); 
                ul.appendChild(li);
            });
            
            listaTarefasDiv.appendChild(ul);
            adicionarListenersToggle(); // Chama o listener do checkbox

        } catch (error) {
            console.error('Erro ao buscar tarefas:', error);
            listaTarefasDiv.innerHTML = `<p style="color:red; text-align: center;">Falha ao carregar as tarefas. ${error.message}</p>`;
        }
    }

    // ---------------------------------------------
    // LÓGICA DE ADIÇÃO DE TAREFA
    // ---------------------------------------------

    formTarefa.addEventListener('submit', async (e) => {
        e.preventDefault(); 
        const dadosForm = {
            nome: document.getElementById('nome').value,
            descricao: document.getElementById('descricao').value,
            prioridade: document.getElementById('prioridade').value,
            data_vencimento: document.getElementById('data_vencimento').value,
            data_hora_inicio: document.getElementById('data_hora_inicio').value,
            data_hora_fim: document.getElementById('data_hora_fim').value,
        };
        
        const formData = new URLSearchParams();
        for (const key in dadosForm) {
            if (dadosForm[key]) {
                formData.append(key, dadosForm[key]);
            }
        }

        try {
            const response = await fetch(ADD_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded' 
                },
                body: formData
            });

            if (response.ok) {
                alert('Tarefa salva com sucesso!');
                formTarefa.reset(); 
                carregarTarefas(); 
            } else {
                alert(`Erro ao salvar tarefa! Status: ${response.status}.`);
            }
        } catch (error) {
            console.error('Erro ao adicionar tarefa:', error);
            alert('Erro de conexão ao salvar tarefa.');
        }
    });

    // Inicia o carregamento quando o DOM estiver pronto
    carregarTarefas();
});