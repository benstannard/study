#### Sources
[Pro Git](https://git-scm.com/book/en/v2)  
[dangit.com](https://dangitgit.com/en)

# Git Basics
```
git init
git clone https://github.com/benstannard/study
git commit -m "Story 182: fix benchmakr for speed"
git commit --amend

git log -p --patch
git log -p --submodule
git log --stat
git log --oneline --decorate
git log --graph
git log -n <limit> -10 --since=2.weeks --until
git show 5eba8a
```

## Working with Remotes
To be able to collaborate on any Git projects, you need to know how to manage your remote repositories. Remote repos are versions of your project that are hosted on the Internet or network somewhere. Collaborating with others involves managing these repos and pushing and pulling data to and from them when you need to share work.  

We can use the shortname in lieu of the whole URL
```
git remote -v
git remote add <shortname> <url>
```

#### Fetching and Pulling from Your Remotes
To get data from remote projects, run:
```
git fetch <remote>      # fetchs any new work that has been pushed to that servce since you cloned/fetched it
git fetch               # only downloads the data to your local repo - you have to merge it mannuall into your work when you're ready
git pull                # command automatically fetch and then merge that remote branch into your current branch
git pull --rebase       # If you want to rebase when pulling: `git config --global pull.rebase "true"`
```

#### Pushing to Your Remotes
When you have your project at a point that you want to share, you have to push it **upstream**.
```
git push <remote> <branch>
git push origin main
```

#### Inspecting a Remote and Renaming
If you want to see more information about a particulare remote, use `git remote show <remote>` commands
```
git remote show <remote>
git remote show origin

git remote rename master main
```

#### Creating Tags
Git supports two types of tags:
1. **lightweight**, very much like a branch that doesn't change - it's just a pointer to a specific commit.
2. **annotated**, stored as full objects in the Git database. They're checksummed; contain the tagger name, email, and date, and a tagging message; and be signed and verifed with GNU Privacy Guard (GPG). It is generally recommed that you create **annotated** tags.
```
# To list/view tags
git tag
git tag -l --list

git tag -a v1.4 -m "my version 1.4"
git show v1.4
```

###### Tagging Later
To tag a older commit, you specify the commit checksum at the end of the command: `git tag -a v1.2 9fceb02`

###### Sharing Tags and Deleting
By default, `git push` doesn't transfer tags to remote servers. You have to explicitly push tags to a shared server after you have created them.
```
git push origin v1.5
git push origin --tags
git tag -d v1.4.1-w
```

###### Checking out Tags
If you need to make changes -- say fixing a bug on a older version - you will generally want to create a branch: `git checkout -b version2 v2.0.0`

## Git Branching
A **branch** is simply a lightweight moveable pointer to one of these commits. Every time the you commit, the `main` branch pointer moves forward automatically. **Branching** means you diverge from the main line of development and continue to do work without messing with that main line. Git encourages a workflow that **branches and merges often**, multiple times in a day. How does Git know what branch you're currently on? It keeps a special pointer called **HEAD**.  

**fast-forward** no divergent work to merge together.  
**merge commit** from a three way merge automattically create a new commit that points to it, it's special, has more than one parent commit.  

#### Branch Management
Older but good [article](https://longair.net/blog/2009/04/16/git-fetch-and-merge/)  
Remote-tracking braches are references to the state of remote branches, think of them as bookmarks. `<remote>/<branch>` `origin/main`
```
git branch                          # simple listing of your current branches
git branch -v                       # To see the last commit on each branch
git branch --merged  --no-merged    # To see branches that have/haven't been merged
git branch -r                       # remote-tracking branches
git ls-remote <remote>

git branch testing
git checkout testing
git checkout -b <newbranchname>
git branch -r ` *remote-tracking branches*
git checkout -b serverfix origin/serverfix`  checkout branch based on remote-tracking branch
```

###### Basic Merging
Your work is complete and ready to merged into `main` branch. Just checkout the branch you wish to merge into and run:
```
git checkout main
git merge iss53
git branch -d iss53
```

###### Basic Merge Conflicts
Git pauses the process while you resolve the conflict. Run:
```
git status
git mergetool
```

###### Changing a branch name
```
git branch --move <old-branch-name> <new-brance-name>
git branch --move master main
git push --set-upstream origin <new-branch-name>
git push origin --delete <old-branch-name>
git push --set-upstream origin main
git branch --all
git push origin --delete master
```

###### Long-Running Branches
`main` branch that entirely stable or code that has been or will be released.  
`develop` branch in parallel that they work from or use to test stability - it isn't always stable, but when it gets to a stable state, it can be merged.  
`iss53` or short-lived branches are merged into `develop` when they're ready and make sure they pass all tests and don't introduce bugs.  

In reality, we're talking about pointers moving up the line of commits you're making. The idea is that your branches are at various levels of stability; when they reach a more stable level, they're merged into the branch above.

###### Pushing
When you want to share a branch with the world, you need to push it up to a remote which you have write access.
```
git push <remote> <branch>
git push origin serverfix       # next time coworker runs `git fetch origin` from the server, they will see the new branch.
```

###### Tracking Branches
Checking out a local branch from a remote-tracking branch automatically creates what is called a "tracking branch". **Tracking branches** are local branches that have a direct relationship to a remote branch. If you're on a tracking branch and run:
```
git pull        # Git automatically knows which server to fetch from and which branch to merge in.
git checkout -b <branch> <remote>/<branch>
git checkout --track <remote>/<branch>
git checkout --track origin/serverfix
git branch -vv`  # to see what tracking branches you have setup
git fetch --all; git branch -vv
```

###### Pulling and Deleting Remote Branch
`git pull` is essentially a `git fetch` immediately followed by a `git merge`.  
Generally it's better to simply use the `fetch` and `merge` commands explicitly as magic of `git pull` can be confusing.  
`git push origin --delete serverfix`  

## Rebasing
In Git, there are two main ways to integrate changes from one branch into another:
1. `merge` - performs a three-way merge.
2. `rebase` - with **`rebase`** you take all the changes that were committed on one branch and replay them on a different branch. The operation goes to the common ancestor of the two branches, the one your on and the one you're rebasing onto, getting the diff, applying changes.  

Rebasing makes for a cleaner history, it looks like a linear history, appears all the work happend in series even though it was parallel. **It's only the history that's different**. Rebasing replays changes from one line of work onto antoher in the order they were introduced. Merging takes the endpoints and merges them together.
```
git checkout experiment
git rebase master           # At this point, you can go back to the master branch ad do a fast-forward merge
git checkout master
git merge experiment
```
**Often** you'll do this to make sure your commits apply cleanly on a remote branch, like contributing to a project you don't maintain. In this case you work in a branch, then rebase your work onto `origin/main` when you're ready to submit your patches to the main project. The maintainer doesn't have to do any integration work - just a fast-forward or a clean apply.

###### More Interestings Rebases
```
git rebase --onto master server client
git checkout master
git merge client
git rebase <basebranch> <topicbranch>
git rebase master server
git checkout master
git merge server
```

###### Perils of Rebasing
**Do not rebase commits that exist outside your repo and that people may have worked on**. Only ever rebase commits that have never left your own computer, you'll be fine. If you rebase commits that have been pushed, and people base work on those commits, you will find trouble. Rebase local changes before pushing to clean up your work, but never rebase anything that you've pushed somewhere.

## [Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
**Submodules** allow you to keep a git repository as a subdirectory of another git repository. This lets you clone another repository into your project and keep your commits separate. Git submodules are simply a reference to another repository at a particular snapshot in time. Git submodules enable a Git repository to incorporate and track version history of external code, submodules are very static and only track specific commits. Submodules do not track git refs or branches and are not automatically updated when the host repository is updated.  

Submodules will add the subproject into a directory named the same as the repository. A new .gitmodules file will be created that contains meta data about the mapping between the submodule project's URL and local directory.  

If often happens that while working on one project, you need to use another project from within it. Perhaps it's a library that a third party developed. A common issue arises in these scenarios: you want to be able to treat the two projects as seperate yet still be able to use one from within the other. Suppose you're creating Atom feeds. Instead of writing your own Atom-generating code, you decide to use a library. Instead of copying the source code into your project, which could make mergin upstream changes difficult, Git addresses this issue using `submodules`.  

###### Starting with Submodules
`git submodule add <url>`  
`git submodule add https://github.com/chaconic/DbConnector`  
`git submodule update --init --recursive`  **use to be on the safe side**, grabs any new or nested submodules.  
`git pull --recurse-submodules`  update with a `git pull`.  

###### Cloning a Project with Submodules
When you clone a project, by default you get the directories that contain submodules, but none of the files within them yet:  
`git clone <url>`  The *submodule* directory will be there, but you must run two commands:  
`git submodule init`  to initalize your locone configuration file, and  
`git submodule update`  to fetch all the data from that project and checkout the appropirate commit listed`  

`git clone --recurse-submodules <url>`  **AS ONE COMMAND ON git clone**  
`git submodule update --init`  combine above steps to initalize, fetch, and checkout any nested submodules.  
`git submodule update --init --recursive` foolproof command of above.  

###### Working on a Project with Submodules
`git submodule update --remote` Git will go into your submodules and fetch and update for you. Git will by default try to update **all**.  

###### Pulling Upstream Changes from the Project Remote
`git pull` does not **update* the submodules.   

<br>
<br>
<br>

## 10.1 Git Internals - Plumbing and Porcelain [Objects, Tree, Commit]
Git is fundamentally a content-addressable filesystem with a VCS user interface written on top of it. All Git objects are stored the same way, just with different types – instead of the string blob, the header will begin with commit or tree. Also, although the blob content can be nearly anything, the commit and tree content are very specifically formatted.  

You mostly use Git with 30 or so subcommands such as checkout, branch, remote, and so on. But because Git was initially a toolkit for a version control system rather than a full user-friendly VCS, it has a number of subcommands that do low-level work and were designed to be chained together UNIX-style or called from scripts. These commands are generally referred to as Git's "plumbing" commands, while the more user-friendly commands are called "porcelain" commands.  

When you run git init in a new or existing directory, Git creates the .git directory, which is where almost everything that Git stores and manipulates is located. If you want to back up or clone your repository, copying this single directory elsewhere gives you nearly everything you need.

#### Four Important parts in .git directory
These are the core parts of Git.
1. the objects directory stores all the content for your database,
2. the refs directory stores pointers into commit objects in that data (branches, tags, remotes and more),
3. the HEAD file points to the branch you currently have checked out,
4. and the index file is where Git stores your staging area information. You'll now look at each of these sections in detail to see how Git operates.

```
$ ls -F1
config		## project specific configuration
description	## only used by GitWeb
HEAD
hooks/
info/		## keep a global exclude pattern for ignored patterns in .gitignore
objects/
refs/
```

#### Git Objects  $ find .git/objects
Git is a content-addressable filesystem. Great. What does that mean?
It means that at the core of Git is a simple key-value data store.
You can insert any kind of content into a Git repository, for which Git will hand you back a unique key you can use later to retrieve that content.

$ git init
Git has initialized the objects directory and created pack and info subdirectories in it, but there are no regular files.
Now, use git hash-object to create a new data object and manually store it in your new Git database

$ echo 'test content' | git hash-object -w --stdin
d670460b4b4aece5915caf5c68d12f560a9fe3e
In its simplest form, git hash-object would take the content you handed to it and merely return the unique key that would be used to store it in your Git database.
The -w option then tells the command to not simply return the key, but to write that object to the database.
Finally, the --stdin option tells git hash-object to get the content to be processed from stdin;
otherwise, the command would expect a filename argument at the end of the command containing the content to be used.

The output from the above command is a 40-character checksum hash.
This is the SHA-1 hash - a checksum of the content you're storing plus a header, which you'll learn about in a bit.
Now you can see how Git has stored your data:

$ find .git/objects -type f
.git/objects/d6/70460b4b4aece5915caf5c68d12f560a9fe3e4
If you again examine your objects directory, you can see that it now contains a file for that new content.
This is how Git stores the content initially — as a single file per piece of content, named with the SHA-1 checksum of the content and its header.
The subdirectory is named with the first 2 characters of the SHA-1, and the filename is the remaining 38 characters.

$ git cat-file
Once you have content in your object database, you can examine that content with the git cat-file command.
This command is sort of a Swiss army knife for inspecting Git objects.
Passing -p to cat-file instructs the command to first figure out the type of content, then display it appropriately:

$ echo 'version 1' > test.txt
$ git hash-object -w test.txt
83baae61804e65cc73a7201a7252750c76066a30

###### Blob
But remembering the SHA-1 key for each version of your file isn't practical.
Plus, you aren't storing the filename in your system - just the content.
This object type is called a blob. You can have Git tell you the object type of any object in Git, given its SHA-1 key, with git cat-file -t:

###### Tree Objects
Tree objects solve the problem of storing the filename and allows you to store a group of files together.
All the content is stored as tree and blob objects.
With trees corresponding to UNIX directory entries and blobs corresponding more or less to inodes or file contents.
A single tree object contains one or more tree entries, each of which contains a SHA-1 pointer to a blob or subtree with its associated mode, type, and filename.
For example, the most recent tree in a project may look something like this:
$ git cat-file -p master^{tree}
$ git write-tree

###### Commit Objects
All Git objects are stored the same way, just with different types - instead of the string blob, the header will begin with commit or tree.
Also, although the blob content can be nearly anything, the commit and tree content are very specifically formatted.

###### Git References [HEAD, tags, remotes]
If you were interested in seeing the history of your repository reachable from commit, say, 1a410e, you could run something like git log 1a410e to display that history,
but you would still have to remember that 1a410e is the commit you want to use as the starting point for that history.
Instead, it would be easier if you had a file in which you could store that SHA-1 value under a simple name so you could use that simple name rather than the raw SHA-1 value.

In Git, these simple names are called "references" or "refs";
You can find the files that contain those SHA-1 values in the .git/refs directory.


# PART2
## Git ##
Git's version control model is based on snapshots.
Git is all about commits: you stage commits, create commits, view old commits, etc.
You can use git checkout to view an old commit by passing in a commit hash.
Understanding the many ways to refer to a commit, you make all of these commands that much more powerful.
The reflog is Git's safety net, records almost every change you make in repository, regardless of whether you commited a snapshot or not.
Git stores branches as a reference to a commit.

## Basics ##
git config --list
git clone // Every version of every file for the history of the project is pulled down by default
.gitignore // you can end patterns with forward slash (/) to specifiy a directory e.g. build/
.gitignore // !lib.a negates a patter if you only want that file and ignore all other .a files
git add *
git remove
git log // displays committed snapshots
git log -n <limit> --oneline
git log --stat
git log -p -2 (last 2) --stat --pretty=oneline
git log --graph --decorate --oneline
git log --author="John Smith" -p hello.py
author is person who originally wrote the work, committer is person who last applied the work

git commit -m 'inital commit'
git add forgotten_file
git commit --amend // You end up with a single commit

git reset HEAD <file> if you commit files you don't want to commit
git checkout -- <file> to discard changes in working directory
git checkout a1e8fb5 hello.py // checkout old version of file
git checkout HEAD hello.py // checkout the most recent version

git remote -v
git fetch [remote-name] // git fetch origin
git fetch // only downloads the data
git pull // automatically fetch and them merge that remote branch into current branch
git pull --rebase // ensure a linear history by preventing unncecassary merge commits.
"I want to put my changes on top of what everybody else has done." Common workflow with --global option
git push [remote-name] [branch-name] // git push origin master
git push <remote> --tags // Tags are not automatically pushed

git checkout -b [branch-name] // create and switch to new branch
git checkout master
git merge [branch-name] // checkout out the branch you wish to merge into and run git merge command
git branch -d [branch-name] // delete the branch, only if merged, use -D if not fully merged
git branch --no-merged // list branchs you have yet to merge
Git add standard conflict-resolution markers to files that have conflicts
After resolving conflicted files, run git add on each file to mark it as resolved. Staging marks it as resolved


## Reverting vs. Resetting ##
Revert generates a new commit that undoes all the changes introduced in <commit>, then apply it to current branch while
reset, the commits are no longer referenced by any ref or reflog.
git reset is one of the only commands that has the potential to lose your work.
Only use reset on local changes.

git reset <file> // remmove <file> from staging area, but leave working directory unchanged
git reset --hard HEAD / if you want to throw away all your uncommitted changes
git reset HEAD`2 // On the commit-level, resetting a way to move the tip of a branch to a different commit
this moves back 2 commits and those will be deleted next time Git performs a garbage collection. Usage of
git reset is a simple way to undo changes that haven't been shared with anyone else. It's your go-to command
to start over locally.

git revert HEAD`2 // undoes a commit by creating a new commit, safe way to undo changes, no chance of re-writing the
commit history

git gc // garbage collection to remove unnecessary objets and compress refs into a single file for more
efficient performances

git push origin master:refs/heads/qa-master // useful for QA teams that need to push their own branches to remote repo
git push origin --delete some-feature // use refspecs for deleting remote branches, you get build-up of dead feature
branchs as your project progress


## git rebase ##
Rebase is one of two Git utilites that specializes integrating changes from one branch onto another.
The other change integration utility is git merge.
Rebase is the process of moving or combining a sequence of commits to a new base commit.

The primary reason for rebase is to maintain a linear project history.
For example, consider a situation where the master branch has progressed since you started working on a feature branch.
You want to get the latest updates to the master branch in your feature branch,
but you want to keep your branch's history clean so it appears as if you've been working off the latest master branch.

Merge directly or rebasing and then merge.
The former option results in a 3-way merge and a merge commit, while
the latter results in a fast-forward merge and a perfectly linear history.

Rebasing is a common way to integrate upstream changes into your local repository. "I want to base my changes on what
everybody has already done." git rebase --interactive gives your the opportunity to alter individual commits in the
process. Like git commit --amend on steroids.

Most developers like to use an interactive rebase to polish a feature branch before merging it into the main code
base. This gives them the opportunity to squash insignificant commits, delete obsolete ones, and make sure everything
else is in order before commit to the "offiical" project history. To everybody else, it will look like the entire
feature was developed in a single series of well-planned commits. It shows in the history of the resulting
master branch.

If you have a long-lived branch that has strayed from master, and you want to rebase against master, merge
conflicts may become more frequent. This is easily remedied by rebasing your branch frequently against master
and making more frequent commits. The --continue and --abort arguments can be passed to advance or reset
the rebase when dealing with conflicts.


## Hooks ##
Git hooks // thinkg of a convenient developer tool rather than a strictly enforced development policy but you can
reject commits that do not conform to some standard using server-side hooks.

Pre-Commit // perhaps run automated tests that make sure commit doesn't break any existing functionality. PEP8?
No arguments are passed to the pre-commit script, exiting with a non-zero status aborts the entire commit.

Post-Commit // can't change outcoem of git commit operations, so it's used primarrily for notification purposes.
If you wanted to log or emal everytime commit happens, this would be the place.

Post-Receive // runs on server instead os user's local machine, it also runs every time any developer pushes their code

Post-Checkout // Nice for clearing out working directory with .pyc files that stick around

Server-side Hooks // can serve as a way to enfore policy bt rejecting certain commits. The output are piped to the
client's console, so it's very easy to send messages back to the developer. Keep in mind these scripts don't return
control of the terminal until they finish executing, so you should be careful about performing long-running operations

Pre-Receive // executed everytime somebody uses git push. The hook runs before any reference are updated.
good place to enfore any kind of development policy that you want.

Post-Recieve // good place to perform notifications.

All Git hooks are ordinary scripts that Git executes when certain events occur in the repository.
Hooks are local and are not copied when you run git clone. Hooks reside in the.git/hooks directory of every Git repository.
Git automatically populates this directory with example scritps but.sample prevents them from executing by default.
You can use any scripting language as long as it can be run as an executable.

Best way to maintain hooks is to store them in actual project directory and create symlink to .git/hooks because
that directory isn't cloned, nor under version control. Git also provides a Template Directory mechanism that makes
it easier to install hooks automatically. The Template Directory gets cloned.


## Refs and the Reflog ##
Understand that may ways to refer to a commit, which Git is all about: commits. The most direct way to reference
a commit is via its SHA-1 hash. This acts as unique ID for each commit. You can find the hash of all your commits
in the git log output.

A ref is an indirect way of referring to a commit. This is Git's internal mechanism of representing branches and tags.
Refs are stored as normal text files in .git/refs directory.

Heads directory defines all of the local branches in your repository. Each filename matches the name of the
corresponding branch, and inside the file you'll find a commit hash. Part of the reason why git branches are so
lightweight compared to SVN is simply matter of writing a commit hash to a new file

There are a few special refs that reside in the top-level .git [HEAD, FETCH_HEAD, ORIG_HEAD, MERGE_HEAD, CHERRY_PICK_HEAD]

A refspec maps a branch in a the local repository to a branch in a remote repository. This makes it possible to manage
remote branches using local Git commands and to configure some advanced git push and git fetch behavior

By adding a few lines to Git configuration file, you can use refspecs to alter the behavior of git fetch, by default
fetches all of the branches in the remote repository. For example, many continuous integration workflows only
care about the master branch, to fetch only the master branch, Refspecs give you complete control over how various
Git commands transfer branches between repositories.

You can also refer to commits relative to another commit. The ~ character lets you reach parent commits.
git show HEAD~2 // ~ always follows first parent of merge commit. use ^ if you want to follow different parent

The REFLOG is Git's safety net. It records almost everything, regardless of whether you commited a snapshot or not.

The HEAD{<n>} lets you reference commits stored in the reflog. You can use this to revert to a state taht would
otherwise be lose. If commits are dangling, meaning no way to ference them - except through the reflog. If you
reset work but relalize that you shouldn't have thrown away all of your work, all you have to do is checkout
the HEAD@{1} commit to get back to the state of your repository before you ran git reset.
