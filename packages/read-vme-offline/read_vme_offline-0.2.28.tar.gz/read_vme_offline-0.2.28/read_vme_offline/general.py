#!/usr/bin/env python3

from fire import Fire
from read_vme_offline.version import __version__

#print("i... module read_vme_offline/ascdf is being run")

import pandas as pd
#import modin.pandas as pd
import tables # here, to avoid a crash when writing pandas
import h5py
import datetime
import subprocess as sp
import numpy as np

import os
import datetime as dt

import matplotlib.pyplot as plt

import ROOT

import sys
# import root_numpy# 2019 is old with newer numpy

import psutil

import datetime as dt

#================ OPERATIONS ON NAMES, INFO ON COLS ROWS
#------------------------------------------------------------------------

def freemem():
    a = psutil.virtual_memory()
    return f"D... AVAIL MEM: {a.available/1024/1024/1024:.2f} GB  ...  used: {a.percent} %"

#------------------------------------------------------------------------

def filename_decomp(filename):
    """
    The ONLY procedure to get the start time from filename
    """
    # should work both with 2021mmdd and  21mmddd
    # returns the start time
    #

    basename = os.path.basename(filename)
    basename = os.path.splitext(basename)[0]
    # start-date
    startd = basename.split("_")[1]
    # start-time
    startt = basename.split("_")[2]

    # 4 digits always
    if len(startd)==6:
        print("D...  compensating 2 digit year to 4 digit year")
        startd="20"+startd

    print("D...  time start MARK=",startd+startt)


    #ok = False
    #try:
    start = dt.datetime.strptime(startd+startt,"%Y%m%d%H%M%S" )
    #ok = True
    print("D... succesfull start with 4 digit year")

    #except:
    #    print("x... year may not by 4 digits")
    #if not(ok):
    #    print("X... trying 2 digits for year")
    #    start = dt.datetime.strptime(startd+startt,"%y%m%d%H%M%S" )

    return start



#------------------------------------------------------------------------

def get_number_of_lines(filename):
    """
    wc to count the lines of ASC
    """
    ps = sp.Popen( ['cat', filename], stdout=sp.PIPE)
    output = sp.check_output(('wc', '-l'), stdin=ps.stdout)
    ps.wait()
    nlines=int(output.decode("utf8").split()[0])
    return nlines

#------------------------------------------------------------------------

def get_number_of_columns(filename):
    """
    omit first 4 lines, take one line and tell
    """
    CMDL = ['head','-n','4', filename]
    ps = sp.Popen( CMDL , stdout=sp.PIPE)
    # print(" ".join(CMDL))
    output = sp.check_output(('tail','-n','1'), stdin=ps.stdout)
    ps.wait()
    ncolumns=len(output.decode("utf8").strip().split())
    if ncolumns==5:
      print(f"D... {ncolumns} cols ... 2020+ version with pile-up info (1/0)")
    elif ncolumns==4:
        print(f"D... {ncolumns} cols  ... 2018 version without extras column, pileup (3/0)")
    else:
        print(f"X... BAD NUMBER OF COLUMNS {ncolumns}")
        sys.exit()
    return ncolumns



#-----------------------------------------------------
def generate_hname(filename, channel):
    """
    create histogram name for ROOT TH
          this will return comment with channel OR run with channel
    works with run_yyddmm_hhmmss.asc
    works with run_yyddmm_hhmmss_.asc
    works with run_yyddmm_hhmmss_comment.asc
    """
    bname = os.path.basename(filename)
    bname2 = os.path.splitext(bname)[0]  #basename

    # get comment part to hname...

    hname = bname2.split("_")[-1]  # last thing should be a comment

    if hname.isdigit(): # NO COMMENT PRESENT NO _ PRESENT  ??? i dont understand that...
        hname = bname2.split("_")[0]
    if len(hname) <2: #  _ PRESENT only
        hname = bname2.split("_")[0]

    if hname[0].isdigit():  # 2Fi1p3_0_1140....
        hname = "h"+hname
    hname = f"{hname}_{channel}"
    return hname


#=============================== CREATE HISTO, TREE

#------------------------------------------------------
def fill_hist( his, narr):
    """
    FILL histogram from np.histogram data.
    simple way bin by bin
    """
    #print(f"D... filling TH  bin by bin ({narr.shape[0]}) bins")
    if len(narr.shape) == 1: # 1D
        for i in range(narr.shape[0]):
            #if narr.shape[0]<6:
            #    print(i, narr[i], "  ", end=";")
            # we start with 0, bin starts with 1 in ROOT
            his.SetBinContent( i+1, narr[i] )

    elif narr.shape[1] == 2: #  2D not tested
        for i in range(narr.shape[0]):
            for j in range(narr.shape[1]):
                his.SetBinContent( i+1, j+1, narr[i][j] )
    #print("D... filling TH DONE")


#------------------------------------------------------------------------
def column_to_histo( dfcol , binmax = 32*1024, himax=32*1024, savename = "", hname = "h1", writeondisk = False , writetxt = True, calibration = None):
    """
    send df["E"] for example
    - converts to numpy array; creates HIST;
    - saves txt
    - updates allhist.root too
    """
    narr = dfcol.to_numpy()
    print(f"D... ========= creating histo {hname} ======= len={len(narr)}; bins=", binmax)
    #print("D... len=", len(narr), narr.dtype, "...  ndarray to np histo")
    #print(dfcol)
    #print(narr)
    his,bins = np.histogram(narr,bins=binmax,range=(0.0,himax) )
    #    print("D... histo:", his)
    #    print("D... bins :", bins)
    del narr

    #
    basename = os.path.basename(savename) # title without path...

    th1f = ROOT.TH1F(hname, basename, binmax, 0 , himax)
    #for i in range(len(his)):
    #    th1f.SetBinContent( i, his[i] )
    #print("D... narr=",narr)

    #print(narr.shape  ,len(narr.shape) )
    #print(narr.shape[0] )
    fill_hist( th1f,  his )

    if not calibration is None:
        CALA = calibration[0]
        CALB = calibration[1]
        Cxmin = th1f.GetXaxis().GetXmin() * CALA + CALB
        Cxmax =th1f.GetXaxis().GetXmax() * CALA + CALB
        th1f.GetXaxis().SetLimits(Cxmin,Cxmax)
    #th1f.Print()

    if (savename!="") and  writeondisk:
        if writetxt:
            print(f"D...          text spectrum = {savename}")
            np.savetxt(savename, his, fmt="%d")
        # rootname = os.path.splitext(savename)[0]+".root"
        rootname = os.path.dirname(savename)
        if len(rootname)>3:
            rootname+="/"
        rootname+="all_histograms.root"
        print("D...          root spectum at", rootname, "name=", hname )
        f = ROOT.TFile(rootname,"UPDATE")
        # print(f"D...          {th1f.GetName():13s} @ {rootname}")
        th1f.Write()
        f.Close()
    endblock(nomem=True)
    return his


#------------------------------------------------------------------------

def save_to_tree(df2, filename, modname="", treename="df"):
    """
     expect 25% of the original size
    """
    outfile =  os.path.splitext(filename)[0] +f"_tree{modname}.root"

    print(f"i... ===============creating and writing {treename} tree", outfile)
    # convert to dict with numpy arrays
    #data = {key: df[key].values for key in ['time', 'E', 'x']}
    data = {key: df2[key].values for key in df2.columns }
    print("D... columns that go to TTree:", df2.columns)
    rdf = ROOT.RDF.MakeNumpyDataFrame( data )
    print(rdf)

    print("D...  snaphost rdf as TTREE to ", outfile)

    start = dt.datetime.now()

    #ROOT.gInterpreter.Declare('ROOT::RDF::RSnapshotOptions opts;')
    #opts.fMode = "update"
    #print("D... opts=,", opts )
    opts = ROOT.RDF.RSnapshotOptions()
    opts.fMode =  "update"
    rdf.Snapshot( treename ,  outfile, "", opts )
    meastime = (dt.datetime.now() - start).total_seconds()
    print(f"D... speed = {get_number_of_lines(filename)/meastime/1000/1000:.3f} Mrows/sec")

    return

#========================== READ; ANALYSIS AND DETECTION ===================


def endblock(nomem=False):
    if not nomem:
        print( freemem() )
    print("D... ","_"*50)






#------------------------------------------------------------------------
def select_channels(df, channels, delete_original = False):
    """
    select channels bu not as view! COPY and DELETE
    """
    print("D... selecting channels:", channels)
    #print( freemem() )
    # CHANNEL (i hope it is sorted)
    if delete_original:
        df1 = df.loc[ df["ch"].isin( channels ) ].copy()
        del df
    else:
        df1 = df.loc[ df["ch"].isin( channels ) ]
    df1.reset_index(inplace=True, drop=True)
    #del df
    if len(df1) ==0 :
        print("X... no data for channels",channels)
        sys.exit(1)
    endblock()
    return df1





def enhance_by_dtus_and_next_E(df):
    print("D... adding dtus and next_E columns")
    print( freemem() )


    print(f"D... broadening table with dt :next event  in t+dtus")
    df['dtus'] = (df.time.shift(-1)-df.time)*1000*1000
    df['dtus'] = df['dtus'].astype('float32') #
    dtusmin = df['dtus'].min()
    dtusmax = df['dtus'].max()
    df.fillna(99999, inplace =True)
    print(f"D... range of time differences (erlang) values : {dtusmin:.3f} us ...  {dtusmax:.3f}  usec." )


    print(f"D... broadening table with dt :prev event  = t - dtus (to enable search for standalones)")
    df['dtuspr'] = (df.time - df.time.shift(+1))*1000*1000
    df['dtuspr'] = df['dtuspr'].astype('float32') #
    dtusminpr = df['dtuspr'].min()
    dtusmaxpr = df['dtuspr'].max()
    df.fillna(99999, inplace =True)
    print(f"D... range of time differences (erlang) values : {dtusminpr:.3f} us ...  {dtusmaxpr:.3f}  usec. PREVIOUS" )

    df['dtus3'] = (df.time.shift(-2)-df.time)*1000*1000 # for triple
    #df.fillna(9999, inplace =True)
    df['dtus3'] = df['dtus3'].astype('float32') #
    dtusmin3 = df['dtus3'].min()
    dtusmax3 = df['dtus3'].max()
    df.fillna(99999, inplace =True)
    print(f"D... range of time differences (erlang) values : {dtusmin3:.3f} us ...  {dtusmax3:.3f}  usec. TRIPLE" )

    df['dtus4'] = (df.time.shift(-3)-df.time)*1000*1000 # for triple
    #df.fillna(9999, inplace =True)
    df['dtus4'] = df['dtus4'].astype('float32') #
    dtusmin4 = df['dtus4'].min()
    dtusmax4 = df['dtus4'].max()
    df.fillna(99999, inplace =True)
    print(f"D... range of time differences (erlang) values : {dtusmin4:.3f} us ...  {dtusmax4:.3f}  usec. QUADRUPLE" )

    df['dtus5'] = (df.time.shift(-4)-df.time)*1000*1000 # for triple
    #df.fillna(9999, inplace =True)
    df['dtus5'] = df['dtus5'].astype('float32') #
    dtusmin5 = df['dtus5'].min()
    dtusmax5 = df['dtus5'].max()
    df.fillna(99999, inplace =True)
    print(f"D... range of time differences (erlang) values : {dtusmin5:.3f} us ...  {dtusmax5:.3f}  usec. PENTUPLE" )




    print(f"D... broadening table - next_E")
    df['next_E'] = (df.E.shift(-1))
    df.fillna(0, inplace=True)
    df['next_E'] = df['next_E'].astype('int32') #

    print(f"D... broadening table - next_E3")  # for triple
    df['next_E3'] = (df.E.shift(-2))
    df.fillna(0, inplace=True)
    df['next_E3'] = df['next_E3'].astype('int32') #

    print(f"D... broadening table - next_E4")  # for triple
    df['next_E4'] = (df.E.shift(-3))
    df.fillna(0, inplace=True)
    df['next_E4'] = df['next_E4'].astype('int32') #

    print(f"D... broadening table - next_E5")  # for triple
    df['next_E5'] = (df.E.shift(-4))
    df.fillna(0, inplace=True)
    df['next_E5'] = df['next_E5'].astype('int32') #




    print(f"D... broadening table - next_ch")
    df['next_ch'] = (df.ch.shift(-1))
    df.fillna(0, inplace=True)
    df['next_ch'] = df['next_ch'].astype('int32') #

    if 'extras' in df.columns:
        print(f"D... broadening table - prev_dtus SATU  previous time")
        df['prev_satu'] = (df.time - df.time.shift(+1))*1000*1000
        #  this says - if no saturation flag=> set 0
        df['prev_satu'] = np.where((df['extras']&1)==1, df['prev_satu'] , 0)
        #  same as
        # df.loc[  (df.extras&1)!=1, 'prev_satu' ] =  0
        #
        #
        df.fillna(0, inplace = True)
        df['prev_satu'] = df['prev_satu'].astype('float32') #

    #----------nice debug print ---------------------
    #print(df)
    endblock()
    return df, dtusmin, dtusmax






#----------------------------------------------------------------------
def pd_detect_zeroes(df, channel,  TIMEWIN_US = 4.2 ):
    """
   1-get the channel only
   2-dtus
    get number of zeroes, single zeroes, double zeroes, standalone zeroes
    -
      2nd phase - SZ and DZ - make one event from these PILEUPs
      3rd phase - create
    """
    print( f"D... detection of zeroes: WINDOW == {TIMEWIN_US} us")
    #print( freemem() )

    # this oneliner doesnt occupy memory ---------------
    # print("D... searching for correlations")

    # I PREPARE SEVERAL VIEWS : only this channel :
    dfz = df[:-1]
    index_names = dfz[  (dfz.ch!=channel)].index
    dfz = dfz.drop(  index_names )
    dfnomu = df # drop the close (cluster) events to count standalones
    index_names = dfnomu[ (dfnomu.ch!=channel)].index
    dfnomu = dfnomu.drop( index_names )

    zeroes = len(  dfz.loc[ (dfz.E==0) ] )
    print( f"TOTAL ZEROES {zeroes}")

    # COMBINED ZEROES
    # ilogic zeroes
    izeroes = len( dfz.loc[ ((dfz.E==0) & (dfz.next_E!=0)) & (dfz.dtus<=TIMEWIN_US) ])
    print( "ilogiczeroes ", izeroes )
    #izeroes = len(df_iz)
    #print(freemem() )
    # single zeroes
    szeroes = len(dfz.loc[ ((dfz.E!=0) & (dfz.next_E==0)) & (dfz.dtus<=TIMEWIN_US) ])
    print( f"singlezeroes = {szeroes} " )


    # STANDAL EVENTS AND LATER ALSO STANDAL ZEROES
    index_names = dfnomu[ (dfnomu.dtus<=TIMEWIN_US) | (dfnomu.dtuspr<=TIMEWIN_US)  ].index
    dfnomu = dfnomu.drop( index_names) # NOT inplace, else it changes the df!!!
    #index_names = dfnomu[ (dfnomu.dtuspr<TIMEWIN_US)  ].index
    ###index_names = dfnomu[ dfnomu.dtuspr<TIMEWIN_US ].index
    #dfnomu = dfnomu.drop( index_names ) # NOT inplace, else it changes the df!!!
    #print(dfnomu)

    print(f"i... I dropped dtus,  remains: len==",len(dfnomu) )
    stazeroes = len( dfnomu.loc[ (dfnomu.E==0)  ])
    print(f" ... of which {stazeroes} is standalone zeroes")


    # playing on clusters----------------------------
    # I drop all nonzero ene and all that are further apart (both sides)

    # this would be more consistently defing the window - each subseq in in WIN

    # ----------- COMPLEMENT TO STANDALONES
    dfz = dfz[~dfz.isin(dfnomu) ].dropna()

    #dfz.reset_index(inplace=True)


    #index_names = dfz[ (dfz.dtus>=TIMEWIN_US) | (dfz.dtuspr>=TIMEWIN_US) ].index  # drop those far
    #dfz = dfz.drop( index_names )
    print(f"dfz (clusters) with all ene      = {len(dfz)}")
    index_names = dfz[ (dfz.E!=0) ].index # drop nonzeroes
    dfz = dfz.drop( index_names )
    print(f"dfz (clusters) with  0  ene only = {len(dfz)}")

    #----------------------- HERE I HAVE PURE ZERO------------------------AND CLUSTERS
    #OK#print(dfz) # here I have all the zeroes (2*dblzero)  11,12; 20,21;


    # I can try to count dblroes
    # this is the start of the cluster and limited to  double clusters


    #dfz.reset_index(inplace=True) # for any games, I need good index

    index_of_doubles = ((dfz.E==0) & (dfz.next_E==0)) & (dfz.dtus<=TIMEWIN_US)& (dfz.dtuspr>TIMEWIN_US) & ( (dfz.next_E3!=0) |  (dfz.dtus3-dfz.dtus>TIMEWIN_US)  )
    dzeroes = len( dfz.loc[ index_of_doubles ])

    print( f"real doublezeroes = {dzeroes}  len of the (zero only) dfz={len(dfz)};  remains to explain {len(dfz)-2*dzeroes} zeroes" )
# 2*dzeroes is not here, since the 2nd part of dbl is not present in in dataframe?/??

    totclusters = len( dfz.loc[ (dfz.dtuspr>TIMEWIN_US)   ])
    print( f"total clusters = {totclusters} ;  number of multiclusters (3+): {totclusters-dzeroes}; exp:{(len(dfz)-2*dzeroes)/(totclusters-dzeroes):.2f}-clusters in average (?!?)" )





    print("______________________ cluster statistics _____ tag and cumulative sum_________")
    dfz['cluster'] = 0
    #dfz.cluster.loc[  (dfz['dtuspr']>TIMEWIN_US) ] = 1 # chaining !!!! not good
    dfz.loc[  (dfz['dtuspr']>TIMEWIN_US) , 'cluster' ] = 1
    #print(dfz)

    dfz['clusum'] = dfz.cluster.cumsum()

    #dfz['dIndex'] = dfz.index
    #dfz.reset_index(inplace=True)
    #dfz['dIndex'] = dfz['dIndex'] - dfz.index
    #print(dfz)
    print(dfz.clusum.value_counts().sort_values(ascending=False).value_counts().sort_index(ascending=False) )
    #print(dfz.dIndex.value_counts().sort_values(ascending=False).value_counts().sort_index(ascending=False) )
    print("______________________ cluster statistics ________________END")




    # print(" ... dropping doublezeroes")

    # index_names = dfz[ ((dfz.E==0) & (dfz.next_E==0)) & (dfz.dtus<=TIMEWIN_US)& (dfz.dtuspr>TIMEWIN_US) & ( (dfz.next_E3!=0) |  (dfz.dtus3-dfz.dtus>TIMEWIN_US)  ) ].index # drop nonzeroes

    # #print(dfz.loc[ index_names] ) # here, only 11, 20, 23 remained.
    # #print(" ... dropping", index_names," = index_names")

    # #slow didnt work for i in index_names: # i need to append Index object
    # last_index = dfz.last_valid_index() # define before, else toooo slow

    # second_index = pd.Index( [ i+1 for i in index_names if i+1<=last_index] )

    # #print(" ... dropping", second_index," = index_names")

    # ###dfz = dfz.drop( dfz[index_of_doubles].index )
    # dfz = dfz.drop( index_names )
    # dfz = dfz.drop( second_index )
    # #pd.set_option('display.max_rows', 100)
    # #print( dfz.tail(100) )


    # totclusters2 = len( dfz.loc[ (dfz.dtuspr>TIMEWIN_US)   ])
    # print( f"total 3+clusters = {totclusters2} ;   exp:{len(dfz)/(totclusters2):.2f}-clusters in average" )







    # # # triple zeroes - time window questionable
    # # tzeroes = len( dfz.loc[ ((dfz.E==0) & (dfz.next_E==0)& (dfz.next_E3==0)) & (dfz.dtus3<2*TIMEWIN_US)& (dfz.dtuspr>TIMEWIN_US) ])
    # # qzeroes = len( dfz.loc[ ((dfz.E==0) & (dfz.next_E==0)& (dfz.next_E3==0)& (dfz.next_E4==0)) & (dfz.dtus4<3*TIMEWIN_US)& (dfz.dtuspr>TIMEWIN_US) ])
    # # # print(freemem() )
    # # pzeroes = len( dfz.loc[ ((dfz.E==0) & (dfz.next_E==0)& (dfz.next_E3==0)& (dfz.next_E4==0)& (dfz.next_E5==0)) & (dfz.dtus5<4*TIMEWIN_US)& (dfz.dtuspr>TIMEWIN_US) ])
    # # # print(freemem() )


    # tzeroes = len( dfz.loc[ (dfz.dtuspr>TIMEWIN_US) & (dfz.dtus3-dfz.dtus<=TIMEWIN_US) & (dfz.dtus4-dfz.dtus3>TIMEWIN_US) ] )

    # index_names = dfz[ (dfz.dtuspr>TIMEWIN_US) & (dfz.dtus3-dfz.dtus<=TIMEWIN_US) & (dfz.dtus4-dfz.dtus3>TIMEWIN_US)  ].index # drop triplets



    # print(" ... dropping triplezeroes")


    # #print(" ... dropping", index_names," = index_names")
    # second_index = pd.Index( [ i+1 for i in index_names if i+1<=last_index] )
    # third_index = pd.Index( [ i+2 for i in index_names if i+2<=last_index] )


    # ###dfz = dfz.drop( dfz[index_of_doubles].index )
    # dfz = dfz.drop( index_names )
    # #print(" ... dropping", second_index," = index_names")
    # dfz = dfz.drop( second_index )
    # #print(" ... dropping", third_index," = index_names")
    # dfz = dfz.drop( third_index )

    # #print(dfz)

    # totclusters3 = len( dfz.loc[ (dfz.dtuspr>TIMEWIN_US)   ])
    # print( f"total 4+clusters = {totclusters3} ;   exp:{len(dfz)/(totclusters3):.2f}-clusters in average" )

    # #DFszeroes =  dfz.loc[ ((dfz.E!=0) & (dfz.next_E==0)) & (dfz.dtus<TIMEWIN_US)  & (dfz.ch==channel)]
    # #print( "singlezeroes \n", DFszeroes )

    # #szeroes = len(df_sz)
    # #print(freemem() )


    # print("______________________ cluster statistics _____i play on sparcity now_________")
    # dfz['cluster'] = 0
    # #dfz.cluster.loc[  (dfz['dtuspr']>TIMEWIN_US) ] = 1 # chaining !!!! not good
    # dfz.loc[  (dfz['dtuspr']>TIMEWIN_US) , 'cluster' ] = 1
    # dfz['clusum'] = dfz.cluster.cumsum()

    # #dfz['dIndex'] = dfz.index
    # #dfz.reset_index(inplace=True)
    # #dfz['dIndex'] = dfz['dIndex'] - dfz.index
    # print(dfz)
    # print(dfz.clusum.value_counts().sort_values(ascending=False).value_counts().sort_index(ascending=False) )
    # #print(dfz.dIndex.value_counts().sort_values(ascending=False).value_counts().sort_index(ascending=False) )
    # print("______________________ cluster statistics ________________END")


    # #zeroes2 = len( dfz[ (dfz.E==0) & (dfz.ch==channel)] )
    # #zeroes = len(df_z)
    # print(freemem() )




    #    D... of which is separated  = {len(dfnomu)-stazeroes:8d}
    output = f"""

    D... total  events (chan={channel}) = {len(df):8d}
    D... total  zeroes (chan={channel}) = {zeroes:8d}   ~  {zeroes/len(df)*100:5.2f}%
    D... total  nonzero(chan={channel}) = {len(df)-zeroes:8d}

    D... standl.zeroes (chan={channel}) = {stazeroes:8d} ~  {stazeroes/len(df)*100:5.2f}%
    D... => zrs@clusters        = {zeroes-stazeroes:8d}    (zeroes that must be in clusters)

    D... double zeroes (chan={channel}) = {dzeroes:8d} ~  {2*dzeroes/len(df)*100:5.2f}% ( % counted correctly 2x)
    D... => zrs@HigherClusters  = {zeroes-stazeroes-2*dzeroes:8d}  (zeroes in longer than 2 clusters)
    D... single zeroes (chan={channel}) = {szeroes:8d} ~  {szeroes/len(df)*100:5.2f}%
    D... ilogic zeroes (chan={channel}) = {izeroes:8d} ~  {izeroes/len(df)*100:5.2f}%
    D... ______________________ end of zero detection
    D...  window {TIMEWIN_US} us   ....  crutial for correct double zeroes detection
"""
    # returns length for now
    endblock()
    return zeroes,dzeroes,szeroes,izeroes,stazeroes,output











#------------------------------------------------------------------------

def pd_read_table(filename, sort = True,  fourcolumns = False):
    """
    READ THE ASC TABLE:   two possibilities:  4 columns OR 5 columns
EARLIER:
         Events[ch][ev].TimeTag, ENERGY,(Events[ch][ev].Energy)>>MAXNBITS, ch
         MAXNBITS 15
Feb 2020+:
       Events[ch][ev].TimeTag, ENERGY,  (Events[ch][ev].Energy)>>MAXNBITS, ch, Events[ch][ev].Extras
       MAXNBITS 15
    >>t,e,PU (1/0) (or 3/0 old)  ,  channel,   Extras(2020+ only)


https://www.npl.washington.edu/TRIMS/sites/sand.npl.washington.edu.TRIMS/files/manuals-documentation/CAENDigitizer_SW_User_Manual_rel.5.pdf

EXTRAS: bit[0] = DEAD_TIME. This is set to 1 when a dead time occurred before this event. The dead time can be due to
either a signal saturation or a full memory status. Check Fig. B.4 and Fig. B.5 for more details
bit[1] = ROLL_OVER. Identify a trigger time stamp roll-over that occurred before this event
bit[2] = TT_RESET. Identify a trigger time stamp reset forced from external signals in S-IN (GPI for Desktop)
bit[3] = FAKE_EVENT. This is a fake event (which does not correspond to any physical event) that identifies a
time stamp roll-over. The roll-over can be due to an external or internal reset. The user can set bit[25]
= 1 of register 0x1n80 to enable the fake-event saving in case of reset from S-IN, and bit[26] = 1 of
register 0x1n80 to enable the fake-event saving in case of internal roll-over. In the first case the event
will have both bit[3] and bit[2] set to 1, while in the second case the event will have both bit[3] and
bit[1] set to 1.
    """
    #print(f"D... fourcolumns=={fourcolumns}")
    #print(f"D... fourcolumns=={fourcolumns}")
    #print(f"D... fourcolumns=={fourcolumns}")
    start = dt.datetime.now()
    df = pd.read_table( filename,
                        names=['time','E','pu','ch','extras'],
                        sep = "\s+",
                        comment="#")

    meastime = (dt.datetime.now() - start).total_seconds()
    print(f"D... table is in memory ...  {get_number_of_lines(filename)/meastime/1000/1000:.3f} Mrows/sec")

    #print(f"D... fourcolumns=={fourcolumns}")

    #print("D... table last timestamp ",df.iloc[-1]["time"]/1e+8, "sec.")
    print( freemem() )
    # drop if 4 column
    df = df.dropna(axis='columns', how='all')


    df['time'] = df['time']/1e+8 # this is correct for 10ns step ADC
    print("D... table last timestamp ",df.iloc[-1]["time"], "sec.")

    #print(df.dtypes)
    df['time'] = df['time'].astype('float64')
    df['E']    = df['E'].astype('int32')
    df['pu']    = df['pu'].astype('int32')
    df['ch']   = df['ch'].astype('int32')
    if 'extras' in df:
        df['extras'] = df['extras'].astype('int32')
    #print("D...    finale types ************************************")
    #print(df.dtypes)

    if fourcolumns:
       print("D... extra operation for four columns ...  FOURCOLUMNS TABLE !!!")
       print(df)
       df['E'] = df['E']+ (df['pu']&1) * 16384
       df['pu'] = df['pu'].apply(lambda x: x >> 1)
       print(df)
    # print(freemem())

    #    df.to_hdf('run'+str(number)+'.h5',
    #              "matrix",
    #              format='t',
    #              data_columns=True,
    #              mode='w')

    # print(freemem() )
    if sort:
        print("D... sorting (after read_table):")
        #print(df)
        df = df.sort_values(by="time")
        #print(df)
        df.reset_index(inplace=True, drop=True)
        #print(df)
        #print( freemem() )

    print("D... table last timestamp ",df.iloc[-1]["time"], "sec.")
    endblock()
    return df





#====================================== MAIN ==================================
#------------------------------------------------------------------------

def main():
    print("D... entry point of general")


#-------------------------------------------------------------------------

if __name__=="__main__":
    print("D... fastread can be called too, from bin_readvme")
    Fire(main)
