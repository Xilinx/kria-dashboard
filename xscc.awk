#!/bin/gawk -f

# From http://vgoenka.tripod.com/unixscripts/xscc.awk.txt

# eXtract Source Code Comment
# Version 1.0

# Usage and other details...

func i(b,c,e,d){
    y=0;
    z=(e=="copyright");
    A=z||(e=="comment");
    B=(!z&&(prune=="copyright"));
    C=D=E="";

    # Check if the file is Jenkinsfile specifically
    if(FILENAME == "Jenkinsfile") {
        b = "jenkinsfile";
    } else if(!b) {
        b=d[split(c,d,".")];
    } else {
        c="";
    }

    if(b==c) C="#";
    else if(b~/^(java|C|cc|h|H|cpp|hpp|cxx|idl|js|groovy|jenkinsfile)$/){
        C="//";
        D="/*";
        E="*/";
    }
    else if(b~/^(c)$/){
        D="/*";
        E="*/";
    }
    else if(b~/^htm|html$/){
        D="<!--";
        E="-->";
    }
    else C="#";
}

func f(g){gsub("\\*","\\*",g);return g}

func h(a,j){
    if(z&&!j&&a) nextfile;
    else if(B&&a){
        if(A&&!j) B=0;
        else if(!A&&j){
            print a;
            y=1;
        }
    }
    else if(j) F=F a;
}

func k(l,t){
    if(l!~/[\x022\x027]/) return "";
    else{
        gsub(/\\.|[^\x022\x027]/,"",l);
        do{
            t=l;
            gsub(/^\x022\x027*\x022|^\x027\x022*\x027/,"",l);
        } while(t!=l);
        if(length(l)) l=substr(l,0,1);
        return l;
    }
}

func p(q,l,n){
    n=index(l,q);
    if(n<=1||(n>1&&substr(l,n-1,1)!="\x05c")) return n;
    else return n+p(q,substr(l,n+1));
}

func o(l,g,r,n){
    n=split(l,r,f(g));
    G=0;
    h(r[1] g,A);
    if(n>1) v(substr(l,length(r[1] g)+1));
}

func s(l,m,g,r,n,q,u){
    u=length(g)+1;
    n=split(l,r,f(g));
    q=k(r[1]);
    if(!length(q)){
        if(m){
            G=1;
            h(r[1],!A);
            h(g,A);
            if(n>1) v(substr(l,length(r[1])+u));
        }
        else{
            h(r[1],!A);
            h(substr(l,length(r[1])+1),A);
        }
    }
    else{
        if(n>1){
            n=p(q,substr(l,length(r[1])+u));
            if(n) n+=length(r[1])+u-1;
        }
        if(n>1){
            h(substr(l,1,n),!A);
            if(n<length(l)) v(substr(l,n+1));
        }
        else print l;
    }
}

func v(l,w,x){
    if(D){
        if(G){
            if(index(l,E)) o(l,E);
            else h(l,A);
        }
        else{
            w=index(l,D);
            if(C&&(x=index(l,C))&&(!w||x<w)) s(l,0,C);
            else if(w) s(l,1,D);
            else h(l,!A);
        }
    }
    else{
        if(index(l,C)) s(l,0,C);
        else h(l,!A);
    }
}

{
    if(FNR==1) {
        i(language,FILENAME,extract);
    }
    if(y) print;
    else{
        F="";
        v($0);
        if(blanklines||F~/[^ ]/) print F;
    }
}