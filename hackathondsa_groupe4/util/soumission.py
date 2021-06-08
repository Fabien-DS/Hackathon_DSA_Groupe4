



def cree_soumission(X_test, pred, use_cible=False, cible=28.392414777526447, use_export=True, nom_fichier_csv='primes2019_soumission.csv'):

    soumission = X_test.copy()
    soumission['prime']=pred
    soumission=soumission[['id','prime']]
    
    if use_cible:
        ini = soumission['prime'].mean()
        soumission['prime']=soumission['prime'].apply(lambda x : x * cible/ini)

    #soumission.rename({'id':'"id"', 'prime':'"prime"'})
    
    if use_export:
        soumission.to_csv('/mnt/data/processed/'+nom_fichier_csv, sep=';', decimal=',', encoding='utf-8', index=False, quotechar='"')

    return soumission
    