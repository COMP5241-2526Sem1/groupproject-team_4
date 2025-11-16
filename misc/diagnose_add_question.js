// Diagnostic script to check Add Question button functionality
(function() {
    console.log('=== Add Question Button Diagnostic ===');
    
    // Check if DOM is loaded
    if (document.readyState === 'loading') {
        console.log('DOM still loading, waiting...');
        document.addEventListener('DOMContentLoaded', runDiagnostics);
    } else {
        console.log('DOM already loaded, running diagnostics...');
        runDiagnostics();
    }
    
    function runDiagnostics() {
        console.log('Running diagnostics...');
        
        // Check if add-question-btn exists
        const addButton = document.getElementById('add-question-btn');
        if (addButton) {
            console.log('✓ Add Question button found:', addButton);
            console.log('  - ID:', addButton.id);
            console.log('  - Class:', addButton.className);
            console.log('  - Text:', addButton.textContent.trim());
            console.log('  - Type:', addButton.type);
            console.log('  - Disabled:', addButton.disabled);
            
            // Check if button has any event listeners
            const events = getEventListeners(addButton);
            console.log('  - Event listeners:', events);
            
            // Check if addQuestion function exists
            if (typeof addQuestion === 'function') {
                console.log('✓ addQuestion function exists');
            } else {
                console.log('✗ addQuestion function NOT found');
            }
            
            // Check if questions-container exists
            const container = document.getElementById('questions-container');
            if (container) {
                console.log('✓ Questions container found:', container);
            } else {
                console.log('✗ Questions container NOT found');
            }
            
            // Test adding event listener manually
            console.log('Attempting to add click event listener...');
            addButton.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('✓ Manual event listener triggered!');
                if (typeof addQuestion === 'function') {
                    console.log('Calling addQuestion function...');
                    addQuestion();
                } else {
                    console.log('addQuestion function not available');
                }
            });
            console.log('Manual event listener added successfully');
            
            // Test button click programmatically
            console.log('Testing programmatic click...');
            setTimeout(() => {
                console.log('Triggering programmatic click in 2 seconds...');
                addButton.click();
            }, 2000);
            
        } else {
            console.log('✗ Add Question button NOT found!');
            console.log('Available buttons:', document.querySelectorAll('button'));
        }
        
        console.log('=== Diagnostic Complete ===');
    }
    
    // Helper function to check event listeners (if available)
    function getEventListeners(element) {
        try {
            // This might not work in all browsers, but try anyway
            const listeners = element._events || {};
            return listeners;
        } catch (e) {
            return 'Unable to detect (browser limitation)';
        }
    }
})();