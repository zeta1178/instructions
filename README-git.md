# SSH Keys
To complete these steps, you will need to sign up for a GitHub Links to an external site.account if you haven't already.

Open Terminal.

To make sure you don’t already have a set of keys on your computer, type the following in your Terminal window. Note: Copying and pasting will not work!

​ `ls –al ~/.ssh`

If no keys pop up, move on to Step 3.
If keys do pop up, check that none of them are listed under id_rsa, like in this image:
SSHKey1

If you find a key with a matching name, you can either overwrite it by following the next steps, or you can use the same key referenced in Step 8. If you decide not to overwrite it, you will need to remember the password tied to your key.
Enter the following command along with your email to generate your keys.

`ssh-keygen –t rsa –b 4096 –C "YOURGITHUBEMAIL@PLACEHOLDER.NET"`

When prompted to enter a file to save the key, press Enter, and then enter a passphrase for your key. Note: You shouldn’t see any characters appear in the window while typing the password. When you’re finished, your window should look like this:

SSHKey2

Link your key to your machine using a tool called the ssh-agent. Run the following command to test whether the ssh-agent is running on your machine: 

`eval "$(ssh-agent –s)"`

Your Terminal window should look like this:

SSHKey3

Run the following command: 

`ssh-add ~/.ssh/id_rsa`

When prompted, enter the passphrase associated with the key. Note: If you’ve forgotten this key, go back to Step 3.

To add the key to GitHub, copy the key to your clipboard by entering the following command:

`pbcopy < ~/.ssh/id_rsa.pub`

You shouldn’t see any kind of message when you run this command. If you do, make sure you entered it correctly.

Note: Do not copy anything else to your clipboard until all steps are completed. Otherwise, you’ll need to enter the copy command again.

Go to GitHub's SSH key settings Links to an external site.. Click "New SSH key."

When the form pops up, enter a name for your computer in the Title input. In the Key input, paste the SSH key you copied in Step 8.

To add GitHub to your computer’s list of acceptable SSH hosts, type the following command in your Terminal window: 

`ssh –T git@github.com`

You should see an RSA fingerprint in your window. Enter "yes" only if it matches the one highlighted in the image below:

SSHKey6