function addForm() {
    const formsetContainer = document.getElementById('formset-container');
    const totalFormsInput = document.getElementById('id_form-TOTAL_FORMS');
    const formIndex = parseInt(totalFormsInput.value);
    console.log('Button clicked!');  // Debugging line

    const managementForm = '{{ form.as_table }}';
    const newForm = managementForm.replace(/__prefix__/g, formIndex);
    console.log('New Form HTML:', newForm);  // Debugging line

    formsetContainer.insertAdjacentHTML('beforeend', newForm);
    totalFormsInput.value = formIndex + 1;
    console.log('New form added. Updated formIndex:', formIndex + 1);  // Debugging line
  }