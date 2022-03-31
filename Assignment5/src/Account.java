public class Account {
    private String accountType;
    private double balance=0.0;
    protected Customer customer;

    public Account(Customer customer,String accountType){
        this.accountType=accountType;
        this.customer=customer;
    }

    public double getBalance() {
        return balance;
    }

    public void setBalance(double balance) {
        this.balance = balance;
    }

    public void deposit(double amount){
        this.setBalance(this.getBalance()+amount);
        System.out.println("Depositing... "+this.getBalance());
        System.out.println("SUCCESSFUL TRANSACTION");
    }

    public void withdraw(double amount){
        System.out.println("Please wait while withdrawing amount"+amount);
        if (this.getBalance()>amount){
            this.setBalance(this.getBalance()-amount);
        }else {
            System.out.println("Amount requested is beyond limit......checking overdraft limit");
            System.out.println("TRANSACTION DENIED. Overdraft limit exceeded.");

        }
    }

    public void display(){
        System.out.println("Customer Account Name:"+customer.getFirstName()+" "+customer.getLastName());
    }


}
