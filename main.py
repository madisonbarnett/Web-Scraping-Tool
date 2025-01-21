import pandas as pd
from colleges import (
    artsAndSciences, 
    communicationAndInformationSciences, 
    communityHealthSciences,
    culverhouseBusiness,
    education,
    engineering,
    humanEnvironmentalSciences,
    lawSchool,
    nursing,
    socialWork
)
    
college_modules = [
    artsAndSciences,
    communicationAndInformationSciences,
    communityHealthSciences,
    culverhouseBusiness,
    education,
    engineering,
    humanEnvironmentalSciences,
    lawSchool,
    nursing, 
    socialWork 
]

combined_df = pd.DataFrame(columns=['Name', 'Image'])

# Go through each college and call collect_data which returns respective df
for module in college_modules:
    college_df = module.collect_data()
    combined_df = pd.concat([combined_df, college_df], ignore_index=True)

combined_df.to_csv('all_colleges_professors.csv', index=False)

