-- CREATE TABLE ExpLine
-- (
-- ID int,
-- Name varchar(255),
-- Description varchar(255),
-- PRIMARY KEY (ID)
-- ); 
-- 
-- 
-- 
-- CREATE TABLE ExpLineActivity
-- (
-- ID int,
-- Name varchar(255),
-- Operation varchar(255),
-- Variant boolean,
-- Optional boolean,
-- ExpLineID int,
-- PRIMARY KEY (ID),
-- FOREIGN KEY (ExpLineID) REFERENCES ExpLine (ID)
-- ); 
-- 
-- CREATE TABLE ExpLineActDependency
-- (
-- ID int,
-- ExpLineActID int,
-- DepExpLineActID int,
-- Variant boolean,
-- Optional boolean,
-- PRIMARY KEY (ID),
-- FOREIGN KEY (ExpLineActID) REFERENCES ExpLineActivity (ID),
-- FOREIGN KEY (DepExpLineActID) REFERENCES ExpLineActivity (ID)
-- ); 
-- 
-- 
-- CREATE TABLE AbstractWorkflow
-- (
-- ID int,
-- Name varchar(255),
-- Description varchar(255),
-- PRIMARY KEY (ID)
-- ); 
-- 
-- 
-- CREATE TABLE AbstractActivity
-- (
-- ID int,
-- Name varchar(255),
-- Operation varchar(255),
-- Description varchar(255),
-- PRIMARY KEY (ID)
-- ); 
-- 
-- 
-- CREATE TABLE Derivation
-- (
-- ID int,
-- ExpLineActID int,
-- AbstractWorkflowID int,
-- AbstractActivityID int,
-- PRIMARY KEY (ID),
-- FOREIGN KEY (ExpLineActID) REFERENCES ExpLineActivity (ID),
-- FOREIGN KEY (AbstractWorkflowID) REFERENCES AbstractWorkflow (ID),
-- FOREIGN KEY (AbstractActivityID) REFERENCES AbstractActivity(ID)
-- ); 
-- 
-- 
-- CREATE TABLE AbstractWorkflowDependency
-- (
-- ID int,
-- DerivationID int,
-- DepDerivationID int,
-- PRIMARY KEY (ID),
-- FOREIGN KEY (DerivationID) REFERENCES Derivation (ID),
-- FOREIGN KEY (DepDerivationID) REFERENCES Derivation (ID)
-- ); 
-- CREATE TABLE ConcreteWorkflow
-- (
-- ID int,
-- PRIMARY KEY (ID)
-- ); 
-- 
-- CREATE TABLE ConcreteActivity
-- (
-- ID int,
-- ConcreteWorkflowID int,
-- Name varchar(255),
-- Operation varchar(255),
-- PRIMARY KEY (ID),
-- FOREIGN KEY (ConcreteWorkflowID) REFERENCES ConcreteWorkflow(ID)
-- );
-- 
-- 
-- CREATE TABLE Instantiation
-- (
-- AbstractWorkflowID int,
-- ConcreteWorkflowID int,
-- AbstractActivityID int,
-- ConcreteActivityID int,
-- FOREIGN KEY (AbstractWorkflowID) REFERENCES AbstractWorkflow (ID),
-- FOREIGN KEY (ConcreteWorkflowID) REFERENCES ConcreteWorkflow (ID),
-- FOREIGN KEY (AbstractActivityID) REFERENCES AbstractActivity(ID),
-- FOREIGN KEY (ConcreteActivityID) REFERENCES ConcreteActivity(ID)
-- ); 

INSERT INTO ExpLine (ID, Name)
VALUES (1, 'SciMG');


INSERT INTO AbstractWorkflow (ID, Name)
VALUES (1, 'Parallel');


INSERT INTO ExpLineActivity (ID, Name, Operation, Variant, Optional, ExpLineID)
VALUES (1, 'PreProcessing', 'Map',False,False,1);

INSERT INTO ExpLineActivity (ID, Name, Operation, Variant, Optional, ExpLineID)
VALUES (2, 'HomologySearch', 'SplitMap',False, False, 1);

INSERT INTO ExpLineActivity (ID, Name, Operation, Variant, Optional, ExpLineID)
VALUES (3, 'InitialPrediction', 'SplitMap', True, False, 1);

INSERT INTO ExpLineActivity (ID, Name, Operation, Variant, Optional, ExpLineID)
VALUES (4, 'Consensus Output', 'MRQuery',False, False, 1);

INSERT INTO ExpLineActivity (ID, Name, Operation, Variant, Optional, ExpLineID)
VALUES (5, 'FinalList', 'MRQuery',False, False, 1);


INSERT INTO AbstractActivity (ID, Name, Operation)
VALUES (1, 'PreProcessing', 'Map');

INSERT INTO AbstractActivity (ID, Name, Operation)
VALUES (2, 'Prodigal', 'SplitMap');

INSERT INTO AbstractActivity (ID, Name, Operation)
VALUES (3, 'MetaGene', 'SplitMap');

INSERT INTO AbstractActivity (ID, Name, Operation)
VALUES (4, 'FragGene', 'SplitMap');

INSERT INTO AbstractActivity (ID, Name, Operation)
VALUES (5, 'Blast', 'SplitMap');

INSERT INTO AbstractActivity (ID, Name, Operation)
VALUES (6, 'Filter1', 'MRQuery');

INSERT INTO AbstractActivity (ID, Name, Operation)
VALUES (7, 'Filter2', 'MRQuery');




INSERT INTO ExpLineActDependency (ID, ExpLineActID,DepExpLineActID, Variant,Optional)
VALUES (2, 1, 2,False,False,1 );

INSERT INTO ExpLineActDependency (ID, ExpLineActID,DepExpLineActID, Variant,Optional)
VALUES (3, 1, 3,False,False,1 );

INSERT INTO ExpLineActDependency (ID, ExpLineActID,DepExpLineActID, Variant,Optional)
VALUES (4, 2, 5,False,False ,1);

INSERT INTO ExpLineActDependency (ID, ExpLineActID,DepExpLineActID, Variant,Optional)
VALUES (5, 3, 4,False,False ,1);

INSERT INTO ExpLineActDependency (ID, ExpLineActID,DepExpLineActID, Variant,Optional)
VALUES (6, 4, 5,False,False ,1);


INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (1,1, 1, 1);

INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (2,2, 1, 2);

INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (3,3, 1, 3);

INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (4,3, 1, 4);

INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (5,3, 1, 5);

INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (6,4, 1, 6);

INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (7,5, 1, 7);

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (1, 1, 2 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (2, 1, 3 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (3, 1, 4 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (4, 1, 5 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (5, 5, 7 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (6, 2, 6 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (7, 3, 6 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (8, 4, 6 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (9, 6, 7 );

INSERT INTO AbstractWorkflow (ID, Name)
VALUES (2,'Split');

UPDATE ExpLineActDependency SET Optional = True WHERE ID = 2;

INSERT INTO ExpLineActivity (ID, Name, Operation, Variant, Optional, ExpLineID)
VALUES (6, 'FastaSplit', 'SplitMap',False, True, 1);

INSERT INTO AbstractActivity (ID, Name, Operation)
VALUES (8, 'FastaSplit', 'SplitMap');

INSERT INTO ExpLineActDependency (ID, ExpLineActID,DepExpLineActID, Variant,Optional,ExpLineID)
VALUES (8, 1, 6 ,False,True,1 );

INSERT INTO ExpLineActDependency (ID, ExpLineActID,DepExpLineActID, Variant,Optional,ExpLineID)
VALUES (9, 6 , 2 ,False,True ,1);


INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (8,1, 2, 1);

INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (9,6, 2, 8);

INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (10,2, 2, 2);

INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (11,3, 2, 3);

INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (12,3, 2, 4);

INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (13,3, 2, 5);

INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (14,4, 2, 6);

INSERT INTO Derivation (ID,ExpLineActID, AbstractWorkflowID, AbstractActivityID)
VALUES (15,5, 2, 7);



INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (10, 8, 9 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (11, 9, 13 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (12, 8, 10 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (13, 8, 11 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (14, 8, 12 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (15, 13, 15);

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (16, 10, 14 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (17, 11, 14 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (18, 12, 14 );

INSERT INTO AbstractWorkflowDependency (ID, DerivationID,DepDerivationID)
VALUES (19, 14, 15 );

INSERT INTO AbstractWorkflow (ID, Name)
VALUES (3, 'Filter');

INSERT INTO AbstractWorkflow (ID, Name)
VALUES (4, 'FilterSplit');


-- -- 
-- -- INSERT INTO ConcreteWorkflow (ID)
-- -- VALUES (1);
-- -- 
-- -- INSERT INTO ConcreteWorkflow (ID)
-- -- VALUES (2);
-- -- 
-- -- INSERT INTO ConcreteActivity (ID, ConcreteWorkflowID, Operation,Name)
-- -- VALUES (1, 1, 'Map', 'Actv1');
-- -- 
-- -- INSERT INTO ConcreteActivity (ID, ConcreteWorkflowID,Operation,Name)
-- -- VALUES (2, 1, 'Map', 'Actv3');
-- -- 
-- -- INSERT INTO ConcreteActivity (ID, ConcreteWorkflowID, Operation,Name)
-- -- VALUES (3, 2, 'Map', 'Actv2');
-- -- 
-- -- INSERT INTO ConcreteActivity (ID, ConcreteWorkflowID, Operation,Name)
-- -- VALUES (4, 2, 'Map', 'Actv3');
-- -- 
-- -- INSERT INTO Instantiation (AbstractWorkflowID, ConcreteWorkflowID, AbstractActivityID, ConcreteActivityID)
-- -- VALUES (1, 1, 1, 1);
-- -- 
-- -- INSERT INTO Instantiation (AbstractWorkflowID, ConcreteWorkflowID, AbstractActivityID, ConcreteActivityID)
-- -- VALUES (1, 1, 3, 2);
-- -- 
-- -- INSERT INTO Instantiation (AbstractWorkflowID, ConcreteWorkflowID, AbstractActivityID, ConcreteActivityID)
-- -- VALUES (2, 2, 2, 3);
-- -- 
-- -- INSERT INTO Instantiation (AbstractWorkflowID, ConcreteWorkflowID, AbstractActivityID, ConcreteActivityID)
-- -- VALUES (2, 2, 3, 4);
-- -- 
-- -- INSERT INTO ExecutionWorkflow (ID, ConcreteWorkflowID, startTime, endTime)
-- -- VALUES (1, 1, 0, 400);
-- -- 
-- -- INSERT INTO ExecutionActivity (ConcreteActivityID, ExecutionWorkflowID, startTime, endTime)
-- -- VALUES (1, 1, 0, 390);
-- -- 
-- -- INSERT INTO ExecutionWorkflow (ID, ConcreteWorkflowID, startTime, endTime)
-- -- VALUES (2, 1, 0, 540);
-- -- 
-- -- INSERT INTO ExecutionActivity (ConcreteActivityID, ExecutionWorkflowID, startTime, endTime)
-- -- VALUES (1, 2, 0, 530);
-- -- 
-- -- INSERT INTO ExecutionWorkflow (ID, ConcreteWorkflowID, startTime, endTime)
-- -- VALUES (3, 2, 0, 730);
-- -- 
-- -- INSERT INTO ExecutionActivity (ConcreteActivityID, ExecutionWorkflowID, startTime, endTime)
-- -- VALUES (3, 3, 0, 720);
-- 
-- 
-- --Listar workflows abstratos derivados da linha de experimento 'Phylogenomic' que possuem variante 'Actv1' do ponto de variação 'vp1'
-- SELECT abstWf.ID
-- FROM AbstractActivity abstActv, AbstractWorkflow abstWf, ExpLine el, Derivation der, VariationPoint vp, Variant var
-- Where el.Name = 'Phylogenomic' AND vp.Name = 'vp1' AND abstActv.Name = 'Actv1'
-- 		AND der.ExpLineID = el.ID AND der.AbstractWorkflowID = abstWf.ID AND der.AbstractActivityID = abstActv.ID
-- 		AND vp.ExpLineID = el.ID AND vp.ID = var.VariationPointID AND var.AbstractActivityID = abstActv.ID;
-- 		
-- --Listar o tempo de execução dos workflows abstratos derivados da linha de experimento 'Phylogenomic' que possuem variante 'Actv1' do ponto de variação 'vp1'
-- SELECT abstWf.ID, (eWf.endTime-eWf.startTime) as time
-- FROM AbstractActivity abstActv, AbstractWorkflow abstWf, ExpLine el, Derivation der, VariationPoint vp, Variant var, ExecutionWorkflow eWf, ExecutionActivity eActv, ConcreteWorkflow concWf, ConcreteActivity concActv, Instantiation inst
-- Where el.Name = 'Phylogenomic' AND vp.Name = 'vp1' AND abstActv.Name = 'Actv1'
-- 		AND der.ExpLineID = el.ID AND der.AbstractWorkflowID = abstWf.ID AND der.AbstractActivityID = abstActv.ID
-- 		AND vp.ExpLineID = el.ID AND vp.ID = var.VariationPointID AND var.AbstractActivityID = abstActv.ID
-- 		AND inst.AbstractWorkflowID = abstWf.ID AND inst.ConcreteWorkflowID = concWf.ID AND inst.AbstractActivityID = abstActv.ID AND inst.ConcreteActivityID = concActv.ID
-- 		AND eWf.ConcreteWorkflowID = concWf.ID AND eActv.ConcreteActivityID = concActv.ID AND eActv.ExecutionWorkflowID = eWf.ID;
-- 		
-- --Qual o tempo médio de execução dos workflows abstratos derivados da linha de experimento 'Phylogenomic' que possuem variante 'Actv1' do ponto de variação 'vp1'
-- SELECT abstWf.ID, avg(eWf.endTime-eWf.startTime) as meantime
-- FROM AbstractActivity abstActv, AbstractWorkflow abstWf, ExpLine el, Derivation der, VariationPoint vp, Variant var, ExecutionWorkflow eWf, ExecutionActivity eActv, ConcreteWorkflow concWf, ConcreteActivity concActv, Instantiation inst
-- Where el.Name = 'Phylogenomic' AND vp.Name = 'vp1' AND abstActv.Name = 'Actv1'
-- 		AND der.ExpLineID = el.ID AND der.AbstractWorkflowID = abstWf.ID AND der.AbstractActivityID = abstActv.ID
-- 		AND vp.ExpLineID = el.ID AND vp.ID = var.VariationPointID AND var.AbstractActivityID = abstActv.ID
-- 		AND inst.AbstractWorkflowID = abstWf.ID AND inst.ConcreteWorkflowID = concWf.ID AND inst.AbstractActivityID = abstActv.ID AND inst.ConcreteActivityID = concActv.ID
-- 		AND eWf.ConcreteWorkflowID = concWf.ID AND eActv.ConcreteActivityID = concActv.ID AND eActv.ExecutionWorkflowID = eWf.ID
-- GROUP BY abstWf.ID;
-- 
-- --listar a media de execução de todos os modelos evolutivos do experimento phylogenomico
-- SELECT abstActv.Name, avg(eWf.endTime-eWf.startTime) as meantime
-- FROM AbstractActivity abstActv, AbstractWorkflow abstWf, ExpLine el, Derivation der, VariationPoint vp, Variant var, ExecutionWorkflow eWf, ExecutionActivity eActv, ConcreteWorkflow concWf, ConcreteActivity concActv, Instantiation inst
-- Where el.Name = 'Phylogenomic' AND vp.Name = 'vp1'
-- 		AND vp.ExpLineID = el.ID AND vp.ID = var.VariationPointID AND var.AbstractActivityID = abstActv.ID
-- 		AND der.ExpLineID = el.ID AND der.AbstractWorkflowID = abstWf.ID AND der.AbstractActivityID = abstActv.ID
-- 		AND inst.AbstractWorkflowID = abstWf.ID AND inst.ConcreteWorkflowID = concWf.ID AND inst.AbstractActivityID = abstActv.ID AND inst.ConcreteActivityID = concActv.ID
-- 		AND eWf.ConcreteWorkflowID = concWf.ID AND eActv.ConcreteActivityID = concActv.ID AND eActv.ExecutionWorkflowID = eWf.ID
-- GROUP BY abstActv.Name;
-- 
-- --Listar quantas vezes cada abordagem de MSA foi selecionada nos workflows abstratos derivados da linha de experimento 'Phylogenomic'
-- SELECT abstActv.Name, count(abstActv.Name)
-- FROM AbstractActivity abstActv, AbstractWorkflow abstWf, ExpLine el, Derivation der, VariationPoint vp, Variant var
-- Where el.Name = 'Phylogenomic' AND vp.Name = 'vp1'
-- 		AND der.ExpLineID = el.ID AND der.AbstractWorkflowID = abstWf.ID AND abstActv.ID = der.AbstractActivityID
-- 		AND vp.ExpLineID = el.ID AND vp.ID = var.VariationPointID AND var.AbstractActivityID = abstActv.ID
-- GROUP BY abstActv.Name;
-- 
-- --Listar as variantes do ponto de variação 'vp1' dos workflows abstratos derivados da linha de experimento 'Phylogenomic'
-- SELECT abstWf.ID, abstActv.Name
-- FROM AbstractActivity abstActv, AbstractWorkflow abstWf, ExpLine el, Derivation der, VariationPoint vp, Variant var
-- Where el.Name = 'Phylogenomic' AND vp.Name = 'vp1'
-- 		AND der.ExpLineID = el.ID AND der.AbstractWorkflowID = abstWf.ID AND abstActv.ID = der.AbstractActivityID
-- 		AND vp.ExpLineID = el.ID AND vp.ID = var.VariationPointID AND var.AbstractActivityID = abstActv.ID;
-- 		
-- 		