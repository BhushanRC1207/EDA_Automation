document.getElementById('analyze-btn').addEventListener('click', function() {
    showLoader();
    hideResults();
    
    fetch('/run-analysis')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            hideLoader();
            displayResults(data);
        })
        .catch(error => {
            hideLoader();
            console.error('Error:', error);
            alert('Error running analysis: ' + error.message);
        });
});

function showLoader() {
    document.getElementById('loader').classList.remove('hidden');
}

function hideLoader() {
    document.getElementById('loader').classList.add('hidden');
}

function hideResults() {
    document.getElementById('results-container').classList.add('hidden');
}

function displayResults(data) {
    document.getElementById('results-container').classList.remove('hidden');
    
    // Display each section
    displayOverview(data.overview);
    displayMissingValues(data.missing_values);
    displayDuplicates(data.duplicates);
    displayStatistics(data.statistics);
    displaySampleData(data.sample_data);
}

function displayOverview(overview) {
    const grid = document.getElementById('overview-grid');
    grid.innerHTML = '';
    
    const stats = [
        { label: 'Total Rows', value: overview.total_rows.toLocaleString() },
        { label: 'Total Columns', value: overview.total_columns },
        { label: 'Numeric Columns', value: overview.numeric_columns },
        { label: 'Categorical Columns', value: overview.categorical_columns },
        { label: 'Memory Usage', value: overview.memory_usage }
    ];
    
    stats.forEach(stat => {
        const statItem = document.createElement('div');
        statItem.className = 'stat-item';
        statItem.innerHTML = `
            <div class="stat-label">${stat.label}</div>
            <div class="stat-value">${stat.value}</div>
        `;
        grid.appendChild(statItem);
    });
}

function displayMissingValues(missing) {
    const summary = document.getElementById('missing-summary');
    const details = document.getElementById('missing-details');
    
    // Summary
    const hasIssues = missing.total_missing_values > 0;
    summary.innerHTML = `
        <div class="alert ${hasIssues ? 'alert-warning' : 'alert-success'}">
            ${hasIssues ? '⚠️ Missing values detected!' : '✅ No missing values found!'}
        </div>
        <div class="summary-item">
            <span class="summary-label">Total Missing Values:</span>
            <span class="summary-value">${missing.total_missing_values.toLocaleString()}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Columns with Missing Values:</span>
            <span class="summary-value">${missing.columns_with_missing}</span>
        </div>
    `;
    
    // Details table
    if (missing.details && missing.details.length > 0) {
        let tableHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Column Name</th>
                        <th>Missing Count</th>
                        <th>Missing %</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        missing.details.forEach(item => {
            tableHTML += `
                <tr>
                    <td><strong>${item.column}</strong></td>
                    <td>${item.missing_count.toLocaleString()}</td>
                    <td>${item.missing_percentage}%</td>
                    <td>
                        <span class="missing-badge ${item.has_missing ? 'missing-yes' : 'missing-no'}">
                            ${item.has_missing ? 'Has Missing' : 'Complete'}
                        </span>
                    </td>
                </tr>
            `;
        });
        
        tableHTML += `
                </tbody>
            </table>
        `;
        
        details.innerHTML = tableHTML;
    }
}

function displayDuplicates(duplicates) {
    const info = document.getElementById('duplicates-info');
    
    const hasDuplicates = duplicates.has_duplicates;
    info.innerHTML = `
        <div class="alert ${hasDuplicates ? 'alert-warning' : 'alert-success'}">
            ${hasDuplicates ? '⚠️ Duplicate records found!' : '✅ No duplicate records found!'}
        </div>
        <div class="summary-item">
            <span class="summary-label">Duplicate Rows:</span>
            <span class="summary-value">${duplicates.duplicate_rows.toLocaleString()}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Duplicate Percentage:</span>
            <span class="summary-value">${duplicates.duplicate_percentage}%</span>
        </div>
    `;
}

function displayStatistics(statistics) {
    const container = document.getElementById('statistics-table');
    
    if (statistics.message) {
        container.innerHTML = `<p class="note">${statistics.message}</p>`;
        return;
    }
    
    if (statistics.numeric_columns && statistics.numeric_columns.length > 0) {
        let tableHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Column</th>
                        <th>Count</th>
                        <th>Mean</th>
                        <th>Std Dev</th>
                        <th>Min</th>
                        <th>25%</th>
                        <th>Median</th>
                        <th>75%</th>
                        <th>Max</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        statistics.numeric_columns.forEach(col => {
            tableHTML += `
                <tr>
                    <td><strong>${col.column}</strong></td>
                    <td>${col.count.toLocaleString()}</td>
                    <td>${col.mean.toLocaleString()}</td>
                    <td>${col.std.toLocaleString()}</td>
                    <td>${col.min.toLocaleString()}</td>
                    <td>${col['25%'].toLocaleString()}</td>
                    <td>${col['50%'].toLocaleString()}</td>
                    <td>${col['75%'].toLocaleString()}</td>
                    <td>${col.max.toLocaleString()}</td>
                </tr>
            `;
        });
        
        tableHTML += `
                </tbody>
            </table>
        `;
        
        container.innerHTML = tableHTML;
    }
}

function displaySampleData(sampleData) {
    const note = document.getElementById('sample-note');
    const table = document.getElementById('sample-table');
    
    note.innerHTML = `📝 ${sampleData.note}`;
    
    if (sampleData.rows && sampleData.rows.length > 0) {
        const columns = Object.keys(sampleData.rows[0]);
        
        let tableHTML = `
            <table>
                <thead>
                    <tr>
                        ${columns.map(col => `<th>${col}</th>`).join('')}
                    </tr>
                </thead>
                <tbody>
        `;
        
        sampleData.rows.forEach(row => {
            tableHTML += '<tr>';
            columns.forEach(col => {
                const value = row[col] !== null && row[col] !== undefined ? row[col] : 'N/A';
                tableHTML += `<td>${value}</td>`;
            });
            tableHTML += '</tr>';
        });
        
        tableHTML += `
                </tbody>
            </table>
        `;
        
        table.innerHTML = tableHTML;
    }
}