USE jerryratdb;
CREATE TABLE IF NOT EXISTS `userdata` (
dataid INT AUTO_INCREMENT PRIMARY KEY,
    age INT NOT NULL,
    job VARCHAR(255) NOT NULL DEFAULT 'unknown'
        CONSTRAINT jobContent CHECK (
            job = 'admin.' OR job = 'blue-collar' OR job = 'entrepreneur' OR
            job = 'housemaid' OR job = 'management' OR job = 'retired' OR
            job = 'self-employed' OR job = 'services' OR job = 'student' OR
            job = 'technician' OR job = 'unemployed' OR job = 'unknown'),
    marital VARCHAR(255) NOT NULL DEFAULT 'unknown'
        CONSTRAINT maritalContent CHECK (
            marital = 'divorced' OR marital = 'married' OR
            marital = 'single' OR marital = 'unknown'),
    education VARCHAR(255) NOT NULL DEFAULT 'unknown'
        CONSTRAINT educationContent CHECK (
            education = 'basic.4y' OR education = 'basic.6y' OR education = 'basic.9y' OR
            education = 'high.school' OR education = 'illiterate' OR education = 'professional.course'
        OR education = 'university.degree' OR education = 'unknown'),
    `default` VARCHAR(10) NOT NULL DEFAULT 'unknown'
        CONSTRAINT defaultAnswer CHECK (
            `default` = 'yes' OR `default` = 'no' OR `default` = 'unknown'
        ),
    housing VARCHAR(10) NOT NULL DEFAULT 'unknown'
        CONSTRAINT housingAnswer CHECK (
            housing = 'yes' OR housing = 'no' OR housing = 'unknown'
        ),
    loan VARCHAR(10) NOT NULL DEFAULT 'unknown'
        CONSTRAINT loanAnswer CHECK (
            loan = 'yes' OR loan = 'no' OR loan = 'unknown'),

    contact VARCHAR(255) NOT NULL
        CONSTRAINT contactMethod CHECK (contact = 'cellular' OR contact ='telephone'),
    `month` VARCHAR(5) NOT NULL
        CONSTRAINT lastContactMonth CHECK (
            `month` = 'oct' OR `month` = 'may' OR `month` = 'apr' OR `month` = 'jun' OR
            `month` = 'feb' OR `month` = 'aug' OR `month` = 'jan' OR `month` = 'jul' OR
            `month` = 'nov' OR `month` = 'sep' OR `month` = 'mar' OR `month` = 'dec'
        ),
    day_of_week VARCHAR(5) NOT NULL
        CONSTRAINT lastContactDay CHECK (
            day_of_week = 'mon' OR day_of_week = 'tue' OR
            day_of_week = 'wed' OR day_of_week = 'thu' OR
            day_of_week = 'fri'),
    duration INT NOT NULL
        CONSTRAINT lastContactDuration CHECK (duration >= 0),
    campaign INT NOT NULL
        CONSTRAINT numContactsDuringCampaign CHECK (campaign >= 0),
    pdays INT NOT NULL
        CONSTRAINT daysPassed CHECK (pdays >= -1),
    previous INT NOT NULL
        CONSTRAINT previousContacts CHECK (previous >= 0),
    poutcome VARCHAR(255) NOT NULL DEFAULT 'nonexistent'
        CONSTRAINT poutcomeContent CHECK (
            poutcome = 'failure' OR
            poutcome = 'nonexistent' OR
            poutcome = 'success'
        ),
    `emp.var.rate` DECIMAL(4, 1) NOT NULL,
    `cons.price.idx` DECIMAL(5, 3) NOT NULL,
    `cons.conf.idx` DECIMAL(3, 1) NOT NULL,
    euribor3m DECIMAL(4, 3) NOT NULL,
    `nr.employed` DECIMAL(5, 1) NOT NULL
);
