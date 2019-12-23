class Callback{
    public:
    virtual void run(int n);
    virtual ~Callback() {}; 
};   
extern Callback * callback;
extern void doSomeWithCallback();
extern void setCallback(Callback * cb);
