SELECT * FROM strategicus.assess_questions;
delete from assess_questions;
ALTER TABLE strategicus.assess_questions AUTO_INCREMENT = 1;
INSERT INTO assess_questions(question, subcomp_id)
VALUES
('Do you differentiate your organization''s work between project work and "regular" work?', 14),
('Do you have a dedicated PMO or similar planning capability?', 14),
('Do you have project stage gates?', 14),
('Do you have multiple tiers of projects based on cost, complexity and risk?', 14),
('Do you define and actively manage project risks?', 14),
('Do you learn from your project mistakes and successfully incorporate those learnings into future projects?', 14),
('Do all of your projects tie back to your organization''s strategic goals?', 14),
('Does your organization have regular project status meetings?', 14),
('Do you have effective project status reports?', 14),
('Does your organization have dedicated project managers for most projects?', 14),
('Are your project managers certified or highly experienced?', 14),
('Are project budgets estimated and planned in a way that enables them to succeed?', 14),
('Are project budgets tracked and reported throughout the life of the project?', 14),
('Are projects planned and balanced for the amount work that needs to be done and the time it will take to do them?', 14),
('Do employees have realistic and achievable project work assignments?', 14),
('Are your vendor partners for each project appropriately reviewed and contracted?', 14),
('Is project planning well coordinated for all projets?', 14),
('Are your projects usually (>75%) delivered on time, on budget and with the right functionality?', 14),
('Does management feel connected to project work?', 14),
('Does every project have an engaged project sponsor?', 14),
('Are those project sponsors the appropriate level of seniority and benefit to enable the project''s success?', 14),
('Is organizational change management considered for every project?', 14),
('Do all projects have a training plan and budget?', 14),
('Do you have a PPM or project planning tool?', 14);

UPDATE `strategicus`.`assess_questions` SET `yes_id` = '2', `no_id` = '99999' WHERE (`question_id` = '1');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '3', `no_id` = '10' WHERE (`question_id` = '2');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '4', `no_id` = '5' WHERE (`question_id` = '3');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '5', `no_id` = '5' WHERE (`question_id` = '4');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '6', `no_id` = '6' WHERE (`question_id` = '5');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '7', `no_id` = '7' WHERE (`question_id` = '6');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '8', `no_id` = '8' WHERE (`question_id` = '7');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '9', `no_id` = '9' WHERE (`question_id` = '8');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '10', `no_id` = '10' WHERE (`question_id` = '9');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '11', `no_id` = '12' WHERE (`question_id` = '10');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '12', `no_id` = '12' WHERE (`question_id` = '11');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '13', `no_id` = '14' WHERE (`question_id` = '12');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '14', `no_id` = '14' WHERE (`question_id` = '13');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '15', `no_id` = '15' WHERE (`question_id` = '14');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '16', `no_id` = '16' WHERE (`question_id` = '15');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '17', `no_id` = '17' WHERE (`question_id` = '16');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '18', `no_id` = '18' WHERE (`question_id` = '17');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '19', `no_id` = '19' WHERE (`question_id` = '18');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '20', `no_id` = '22' WHERE (`question_id` = '19');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '21', `no_id` = '22' WHERE (`question_id` = '20');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '22', `no_id` = '22' WHERE (`question_id` = '21');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '23', `no_id` = '24' WHERE (`question_id` = '22');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '24', `no_id` = '24' WHERE (`question_id` = '23');
UPDATE `strategicus`.`assess_questions` SET `yes_id` = '99999', `no_id` = '99999' WHERE (`question_id` = '24');
