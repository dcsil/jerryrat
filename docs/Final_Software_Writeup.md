1. Login and registration: 

   - All features will only be shown to logged in users.
2. Data Entry Page:

   - This is where the user uploads his/her data for the machine learning model to make prediction with.
   - The uploaded data will be automatically fed to the pretrained Machine Learning model.
   - Currently the app only takes data with a fixed format shown in the description, a set of test dataset is provided for you for testing purpose in the MVP-Test folder.
   - Currently the app only accepts a csv file as input.
   - Since we are not allowed to purchase a higher level JawsDB plan due to their strange policy (a user can't choose a plan for more than 10$ if he/she hasn't made a payment before), please make sure the uploaded file is not too big (which may possibly exceeds the allowed limit!)

3. Calling Operation Page:
   - The prediction is reflected here. User can check a piece of data simply by clicking it.
   - If the user want, he/she can download that specific campaign prediction by clicking the "Download" button.
4. Analytic Dashboard:
   - Considering the accessibility of color blindness, when the user hover his/her mouse over the bar chart, a tag will show up indicating each segments' meaning.
   - The user can zoom the graph. The user can download the graphs as well.
   - First 7 graphs are fixed and can not be removed.
   - The user can add or delete customized graphs.
5. Model Control:
   - User can change machine learning model's configurations here.
   - User can retrain the model with his/her own configuration here.

