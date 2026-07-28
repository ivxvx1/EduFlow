    //========Calendar======

        document.addEventListener('DOMContentLoaded', function() {
            const calendarEl = document.getElementById('calendar');
            const taskModal = document.getElementById('task-modal');
            const closeBtn = document.querySelector('.close-btn');

            const flashMessages = document.querySelectorAll('.flash-messages .message');
            flashMessages.forEach(msg => {
                setTimeout(() => {
                    msg.style.opacity = '0';
                    msg.style.transition = 'opacity 0.5s ease-out';
                    
                    setTimeout(() => msg.remove(), 500); 
                }, 2000); 
            });



            const eventsDataElement = document.getElementById('django-tasks');
            const eventsJsonString = eventsDataElement ? eventsDataElement.getAttribute('data-tasks-json') : '[]';
            let allEvents = [];
            try {
                allEvents = JSON.parse(eventsJsonString);
            } catch (e) {
                console.error("Error parsing Django events data:", e);
            }
        
            const calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                height: 600,
                selectable: true,
                events: allEvents, 
                

                dateClick: function(info) {
                    taskModal.style.display = "flex";
                },
                eventClick: function(info) {
                    taskModal.style.display = "flex";
                },
            });
        
            calendar.render();
        

            closeBtn.addEventListener('click', () => taskModal.style.display = "none");
            window.addEventListener('click', (event) => {
                if (event.target === taskModal) {
                    taskModal.style.display = "none";
                }
            });
        });

        //============dashboard========
                document.addEventListener('DOMContentLoaded', function() {
            
            const flashMessages = document.querySelectorAll('.flash-messages .message');
            
            flashMessages.forEach(msg => {
                setTimeout(() => {
                    if (msg) {
                        msg.remove(); 
                    }
                }, 5000); 
            });

            var editButton = document.getElementById('editCourseButton');
            var formContainer = document.getElementById('editCourseFormContainer');

            if (editButton && formContainer) {
                editButton.addEventListener('click', function(e) {
                    
                    
                    if (formContainer.style.display === 'none' || formContainer.style.display === '') {
                        
                       
                        if (confirm('Are you sure you want to edit the details of this course?')) {
                            formContainer.style.display = 'block';
                            editButton.innerHTML = '<i class="fa-solid fa-xmark"></i> Cancel Edit';
                            editButton.classList.remove('primary');
                            editButton.classList.add('ghost');
                        }
                        
                    } else {
                        
                        formContainer.style.display = 'none';
                        editButton.innerHTML = '<i class="fa-solid fa-pen-to-square"></i> Edit Details';
                        editButton.classList.remove('ghost');
                        editButton.classList.add('primary');
                    }
                });
            } 
            const urlParams = new URLSearchParams(window.location.search);
            const editUnitId = urlParams.get('edit_unit');
            const editAssessmentId = urlParams.get('edit_assessment');
            const manageCourse = urlParams.get('manage');

            if (manageCourse) {
                const managerSection = document.getElementById('course-manager');
                if (managerSection) {
                    managerSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
            
            if (editUnitId) {
                const editUnitForm = document.getElementById('unit-edit-form-' + editUnitId);
                if (editUnitForm) {
                    editUnitForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }

            
            if (editAssessmentId) {
                const editAssessmentForm = document.getElementById('assessment-edit-form-' + editAssessmentId);
                if (editAssessmentForm) {
                    editAssessmentForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });

    $(document).ready(function () {
        
        // ==================  (coursesTable and courseReport) ==================
        $("#coursesTable").DataTable({
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    title: 'Courses Export'
                },
                {
                    extend: 'pdfHtml5',
                    title: 'Courses Export',
                    orientation: 'portrait',
                    pageSize: 'A4'
                }
            ],
            pageLength: -1,
            lengthMenu: [5, 10, 25, 50, -1],
            ordering: true,
            searching: true
        });
    });