import joblib
from django.shortcuts import render
from .forms import ChildMortalityFormForm

# Load the pre-trained model
model = joblib.load(
    'C:/Users/tlche/OneDrive/Documents/GitHub/Predictive-Analytics-for-Tuberculosis-TB-Incidence-and-Treatment-Adherence/random_forest_model.pkl')


def dashboard(request):
    prediction = None
    if request.method == 'POST':
        form = ChildMortalityFormForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Ensure to capture all the required fields
            X_input = [
                int(data['cause_of_fistula']),      # s1205
                data['number_of_children'],         # v218
                int(data['current_pregnancy']),     # v220
                # v219 (Add this to the form)
                data['number_of_living_children'],
                int(data['marital_status']),        # v502
                # v224 (Add this to the form)
                int(data['entries_in_birth_history']),
                # v201 (Add this to the form)
                int(data['total_children_ever_born']),
                int(data['age_at_first_sex']),      # v525
                # v535 (Add this to the form)
                int(data['ever_been_married'])
            ]

            prediction = model.predict([X_input])[0]

            return render(request, 'dashboard/dashboard.html', {'form': form, 'prediction': prediction})
        else:
            print("Form errors:", form.errors)
    else:
        form = ChildMortalityFormForm()

    return render(request, 'dashboard/dashboard.html', {'form': form, 'prediction': prediction})


def success(request):
    prediction = request.GET.get('prediction')
    return render(request, 'dashboard/success.html', {'prediction': prediction})