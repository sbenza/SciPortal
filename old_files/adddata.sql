INSERT INTO addline_experimentline (explineid, tag)
VALUES (1, 'Phylogenomic');

INSERT INTO addline_AbstractWorkflow (awkfid)
VALUES (1);

INSERT INTO addline_AbstractWorkflow (awkfid)
VALUES (2);

INSERT INTO addline_AbstractActivity (aactid, tag, Operation)
VALUES (1, 'Actv1', 'Map');

INSERT INTO addline_AbstractActivity (aactid, tag, Operation)
VALUES (2, 'Actv2', 'Map');

INSERT INTO addline_AbstractActivity (aactid, tag, Operation)
VALUES (3, 'Actv3', 'Map');

INSERT INTO addline_Variantactivity (vactid, aactid_id, vpointid_id)
VALUES (1, 1, 1);

INSERT INTO addline_Variantactivity (vactid, aactid_id, vpointid_id)
VALUES (2, 2, 1);

INSERT INTO addline_VariationPoint (vpointid, explineid_id, tag, Optional)
VALUES (1, 1, 'vp1', 'false');

INSERT INTO addline_InvariantActivity (iactid, explineid_id, aactid_id, Optional)
VALUES (1, 1, 3, 'false');

INSERT INTO addline_Derivation (explineid_id, awkfid_id, aactid_id)
VALUES (1, 1, 1);

INSERT INTO addline_Derivation (explineid_id, awkfid_id, aactid_id)
VALUES (1, 1, 3);

INSERT INTO addline_Derivation (explineid_id, awkfid_id, aactid_id)
VALUES (1, 2, 2);

INSERT INTO addline_Derivation (explineid_id, awkfid_id, aactid_id)
VALUES (1, 2, 3);

INSERT INTO addline_ConcreteWorkflow (cwkfid)
VALUES (1);

INSERT INTO addline_ConcreteWorkflow (cwkfid)
VALUES (2);

INSERT INTO addline_ConcreteActivity (cactid, cwkfid_id, tag, Operation)
VALUES (1, 1, 'Map', 'Actv1');

INSERT INTO addline_ConcreteActivity (cactid, cwkfid_id, tag, Operation)
VALUES (2, 1, 'Map', 'Actv3');

INSERT INTO addline_ConcreteActivity (cactid, cwkfid_id, tag, Operation)
VALUES (3, 2, 'Map', 'Actv2');

INSERT INTO addline_ConcreteActivity (cactid, cwkfid_id, tag, Operation)
VALUES (4, 2, 'Map', 'Actv3');

INSERT INTO addline_Instantiation (awkfid_id, cwkfid_id, aactid_id, cactid_id)
VALUES (1, 1, 1, 1);

INSERT INTO addline_Instantiation (awkfid_id, cwkfid_id, aactid_id, cactid_id)
VALUES (1, 1, 3, 2);

INSERT INTO addline_Instantiation (awkfid_id, cwkfid_id, aactid_id, cactid_id)
VALUES (2, 2, 2, 3);

INSERT INTO addline_Instantiation (awkfid_id, cwkfid_id, aactid_id, cactid_id)
VALUES (2, 2, 3, 4);

INSERT INTO addline_ExecutionWorkflow (ewkfid, cwkfid_id, startTime, endTime)
VALUES (1, 1, 0, 400);

INSERT INTO addline_ExecutionActivity (cwkfid_id, ewkfid_id, startTime, endTime)
VALUES (1, 1, 0, 390);

INSERT INTO addline_ExecutionWorkflow (ewkfid, cwkfid_id, startTime, endTime)
VALUES (2, 1, 0, 540);

INSERT INTO addline_ExecutionActivity (cwkfid_id, ewkfid_id, startTime, endTime)
VALUES (1, 2, 0, 530);





		