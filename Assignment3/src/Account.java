public class Account {
    private String accountType;
    private double balance;
    private Customer customer;

    public Account(){};
    public Account(Customer customer,String accountType){
        this.customer=customer;
        this.accountType=accountType;
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
        if (this.getBalance()>amount)
        {
            this.setBalance(this.getBalance() - amount);
            System.out.println("Please wait while withdrawing amount: "+this.getBalance());
            System.out.println("SUCCESSFUL TRANSACTION");
        }else {
            System.out.println("Please wait while withdrawing amount: "+amount);
            System.out.println("TRANSACTION DENIED. Insufficient funds.");
        }
    }

    public void display(){
        System.out.println("Customer Account Name: "+customer.getFirstName()+" "+customer.getLastName());
        System.out.println(this.accountType+" account balance: "+this.getBalance());
    }

}
