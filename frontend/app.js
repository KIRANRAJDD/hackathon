document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const btnText = generateBtn.querySelector('.btn-text');
    const loader = generateBtn.querySelector('.loader');
    const codeInput = document.getElementById('code-input');
    const langSelect = document.getElementById('language-select');
    
    const welcomeState = document.getElementById('welcome-message');
    const resultsContainer = document.getElementById('results-container');
    
    // Tab switching logic
    const tabs = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.add('hidden'));
            
            tab.classList.add('active');
            document.getElementById(tab.dataset.target).classList.remove('hidden');
        });
    });

    generateBtn.addEventListener('click', async () => {
        const code = codeInput.value.trim();
        if (!code) {
            alert('Please paste some code first!');
            return;
        }

        // Set Loading state
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');
        generateBtn.style.opacity = '0.7';
        generateBtn.disabled = true;

        try {
            const response = await fetch('http://127.0.0.1:8000/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    code: code,
                    language: langSelect.value
                })
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Failed to generate tests');
            }

            const data = await response.json();
            
            // Render outputs
            document.getElementById('out-summary').innerText = data.results.summary;
            
            const scenariosList = document.getElementById('out-scenarios');
            scenariosList.innerHTML = '';
            (data.results.scenarios || []).forEach(sc => {
                const li = document.createElement('li');
                li.innerText = sc;
                scenariosList.appendChild(li);
            });

            document.getElementById('out-unit').innerText = data.results.unit_tests || 'No unit tests generated.';
            document.getElementById('out-integration').innerText = data.results.integration_tests || 'No integration tests generated.';
            document.getElementById('out-edge').innerText = data.results.edge_cases || 'No edge cases generated.';

            // Show results
            welcomeState.classList.add('hidden');
            resultsContainer.classList.remove('hidden');

        } catch (error) {
            alert("Error: " + error.message);
        } finally {
            // Unset loading state
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
            generateBtn.style.opacity = '1';
            generateBtn.disabled = false;
        }
    });

    // Make textarea support tab indentation
    codeInput.addEventListener('keydown', function(e) {
      if (e.key == 'Tab') {
        e.preventDefault();
        var start = this.selectionStart;
        var end = this.selectionEnd;
        this.value = this.value.substring(0, start) +
          "    " + this.value.substring(end);
        this.selectionStart =
          this.selectionEnd = start + 4;
      }
    });
});
