document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('resumeAnalysisForm');
    const analysisResults = document.getElementById('analysisResults');
    const scoreDetails = document.getElementById('scoreDetails');
    const qualityDetails = document.getElementById('qualityDetails');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Reset previous results
        analysisResults.style.display = 'none';
        scoreDetails.innerHTML = '';
        qualityDetails.innerHTML = '';

        // Get form data
        const resumeFile = document.getElementById('resumeFile').files[0];
        const jobTitle = document.getElementById('jobTitle').value;

        // Validate inputs
        if (!resumeFile) {
            alert('Please upload a resume PDF');
            return;
        }
        if (!jobTitle) {
            alert('Please select a job title');
            return;
        }

        // Create form data
        const formData = new FormData();
        formData.append('resumeFile', resumeFile);
        formData.append('jobTitle', jobTitle);

        // Show loading state
        form.querySelector('button').disabled = true;
        form.querySelector('button').innerHTML = 'Analyzing...';

        // Send analysis request
        fetch('/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Handle successful analysis
            analysisResults.style.display = 'block';

            // Display Job Relevance Scores
            if (data.job_relevance) {
                const relevance = data.job_relevance;
                const scoreHtml = `
                    <p><strong>Overall Score:</strong> ${relevance.overall_score}/100</p>
                    <ul>
                        <li><strong>Skill Score:</strong> ${relevance.skill_score}/40</li>
                        <li><strong>Experience Score:</strong> ${relevance.experience_score}/30 
                            (${relevance.total_years_experience} total years)</li>
                        <li><strong>Education Score:</strong> ${relevance.education_score}/30</li>
                    </ul>
                    <p><strong>Matched Skills:</strong> ${relevance.matched_skills.join(', ')}</p>
                    ${relevance.roles_identified ? `<p><strong>Roles Identified:</strong> ${relevance.roles_identified.join(', ')}</p>` : ''}
                `;
                scoreDetails.innerHTML = scoreHtml;
            }

            // Display Quality Metrics
            if (data.quality_metrics) {
                const metrics = data.quality_metrics;
                const qualityHtml = `
                    <ul>
                        <li><strong>Word Count:</strong> ${metrics.word_count}</li>
                        <li><strong>Action Verbs Used:</strong> ${metrics.action_verb_count} 
                            (${metrics.action_verbs_used.join(', ')})</li>
                        <li><strong>Quantifiable Achievements:</strong> ${metrics.quantifiable_achievements}</li>
                        <li><strong>Present Required Sections:</strong> ${metrics.present_required_sections.join(', ')}</li>
                        ${metrics.missing_required_sections.length > 0 ? 
                            `<li><strong>Missing Required Sections:</strong> ${metrics.missing_required_sections.join(', ')}</li>` : ''}
                        <li><strong>Present Optional Sections:</strong> ${metrics.present_optional_sections.join(', ')}</li>
                        <li><strong>Potential Misspellings:</strong> ${metrics.potential_misspellings}</li>
                    </ul>
                `;
                qualityDetails.innerHTML = qualityHtml;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while analyzing the resume');
        })
        .finally(() => {
            // Reset button state
            form.querySelector('button').disabled = false;
            form.querySelector('button').innerHTML = 'Analyze Resume';
        });
    });
});